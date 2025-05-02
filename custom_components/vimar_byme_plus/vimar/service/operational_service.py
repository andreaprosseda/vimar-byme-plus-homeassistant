from collections.abc import Coroutine
import time
from typing import Any

from websocket import WebSocketConnectionClosedException

from ..client.web_service.sync_session_phase import SyncSessionPhase
from ..client.web_service.ws_attach_phase import WSAttachPhase
from ..database.database import Database
from ..model.component.vimar_component import VimarComponent
from ..model.enum.action_type import ActionType
from ..model.enum.integration_phase import IntegrationPhase
from ..model.exceptions import VimarErrorResponseException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.web_socket.base_request import BaseRequest
from ..model.web_socket.base_request_response import BaseRequestResponse
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..scheduler.keep_alive_handler import KeepAliveHandler
from ..utils.logger import log_info
from .handler.action_handler.action_handler import ActionHandler
from .handler.error_handler.error_handler import ErrorHandler
from .handler.message_handler.message_handler import MessageHandler

type Update = Coroutine[Any, Any, None]


class OperationalService:
    gateway_address: str
    session_port: int
    attach_port: int | None = None

    gateway_info: GatewayInfo
    update_callback: Update

    _message_handler: MessageHandler
    _action_handler: ActionHandler
    _error_handler: ErrorHandler
    _keep_alive_handler: KeepAliveHandler

    _web_socket: WSAttachPhase = None
    _user_repo = Database.instance().user_repo

    def __init__(self, gateway_info: GatewayInfo, callback: Update) -> None:
        """Initialize Vimar intagration."""
        self.gateway_address = gateway_info.address
        self.session_port = gateway_info.port
        self.gateway_info = gateway_info
        self.update_callback = callback
        self._action_handler = ActionHandler()
        self._error_handler = ErrorHandler(gateway_info)
        self._message_handler = MessageHandler(gateway_info)
        self._keep_alive_handler = KeepAliveHandler()

    def connect(self):
        """Handle the connection Vimar WebSocket connection."""
        try:
            self.clean()
            self.sync_session_phase()
            self.async_attach_phase()
        except Exception as exc:
            if self._error_handler.is_temporary_error(exception=exc):
                log_info(__name__, "Waiting 60 seconds before reconnecting...")
                time.sleep(60)
                self.connect()
            else:
                raise VimarErrorResponseException(exc) from exc

    def send_action(self, component: VimarComponent, action_type: ActionType, *args):
        """Send a request coming from HomeAssistant to Gateway."""
        actions = self._action_handler.get_actions(component, action_type, *args)
        message = self._message_handler.start_do_action(actions)
        self.send_message(message)

    def send_get_status(self, idsf: int):
        """Send a request coming from HomeAssistant to Gateway."""
        message = self._message_handler.start_get_status(idsf)
        self.send_message(message)

    def send_message(self, message: BaseRequest):
        """Send a request coming from HomeAssistant to Gateway."""
        if not self._web_socket:
            raise WebSocketConnectionClosedException
        self._web_socket.send(message)

    def sync_session_phase(self):
        """Handle SessionPhase interaction."""
        log_info(__name__, "Starting Operational | Session Phase...")
        config = self._get_config()
        handler = self._message_handler
        client = SyncSessionPhase(config, handler)
        self.attach_port = client.connect()
        log_info(__name__, "Operational | Session Phase Done!")

    def async_attach_phase(self):
        """Handle AttachPhase interaction."""
        log_info(__name__, "Starting Operational | Attach Phase...")
        config = self._get_config_for_attach_phase()
        self._web_socket = WSAttachPhase(config)
        self._web_socket.connect()

    def clean(self):
        self.attach_port = None
        self._message_handler.clean()

    def on_attach_connection_opened(self):
        self._keep_alive_handler = KeepAliveHandler()
        self._keep_alive_handler.set_handler(self.send_keep_alive)

    def on_attach_message_received(
        self, message: BaseRequestResponse
    ) -> BaseRequestResponse:
        response = self._message_handler.message_received(message)
        self.trigger_changes(message)
        self.handle_keep_alive(response)
        return response

    def on_attach_error_message_received(
        self,
        last_client_message: BaseRequestResponse,
        last_server_message: BaseRequestResponse,
        exception: Exception,
    ) -> BaseRequestResponse:
        response = self._error_handler.error_message_received(
            last_client_message, last_server_message, exception
        )
        self.handle_keep_alive(response)
        return response

    def on_attach_close_callback(self, message: BaseRequestResponse):
        self._keep_alive_handler.stop()
        self.attach_port = None
        if isinstance(message, BaseRequest):
            seconds_to_wait = self._get_seconds_to_wait(message)
            message = f"Waiting {seconds_to_wait!s} seconds before reconnecting..."
            log_info(__name__, message)
            time.sleep(seconds_to_wait)
            self.connect()
        if self._error_handler.is_temporary_error(None, message):
            log_info(__name__, "Temporary Error detected, reconnecting...")
            self.connect()

    def trigger_changes(self, message: BaseRequestResponse):
        if not self.update_callback:
            return

        phase = IntegrationPhase.get(message.function)
        change_phase = IntegrationPhase.CHANGE_STATUS
        if isinstance(message, BaseRequest) and phase == change_phase:
            self.update_callback()

    def handle_keep_alive(self, message: BaseRequestResponse):
        if message:
            self._keep_alive_handler.reset()

    def send_keep_alive(self):
        try:
            message = self._message_handler.start_keep_alive()
            self.send_message(message)
            self._keep_alive_handler.reset()
        except WebSocketConnectionClosedException:
            self.disconnect()

    def _get_config_for_attach_phase(self) -> WebSocketConfig:
        config = self._get_config()
        config.user_credentials = self._user_repo.get_current_user()
        config.on_open_callback = self.on_attach_connection_opened
        config.on_message_callback = self.on_attach_message_received
        config.on_error_message_callback = self.on_attach_error_message_received
        config.on_close_callback = self.on_attach_close_callback
        return config

    def _get_config(self) -> WebSocketConfig:
        config = WebSocketConfig()
        config.gateway_info = self.gateway_info
        config.address = self.gateway_address
        config.port = self.attach_port if self.attach_port else self.session_port
        return config

    def _get_seconds_to_wait(self, request: BaseRequest) -> int:
        if request and request.args:
            return int(request.args[0].get("value", 0))
        self.disconnect()

    def disconnect(self):
        log_info(__name__, "Terminating the execution...")
        self._keep_alive_handler.stop()
        if self._web_socket:
            self._web_socket.close()
            self._web_socket = None
