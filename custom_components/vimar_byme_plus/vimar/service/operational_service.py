import os
import time
from typing import Callable, Optional

from websocket import WebSocketApp, WebSocketConnectionClosedException

from ..client.web_service.sync_attach_phase import SyncAttachPhase
from ..client.web_service.sync_session_phase import SyncSessionPhase
from ..client.web_service.ws_attach_phase import WSAttachPhase
from ..database.database import Database
from ..model.gateway.gateway_info import GatewayInfo
from ..model.web_socket.base_request import BaseRequest
from ..model.web_socket.base_request_response import BaseRequestResponse
from ..model.web_socket.base_response import BaseResponse
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..model.exceptions import VimarErrorResponseException
from ..scheduler.keep_alive_handler import KeepAliveHandler
from ..utils.logger import log_info
from ..utils.thread import Timer
from .error_handler.error_handler import ErrorHandler
from .message_handler.message_handler import MessageHandler
from ..utils.thread import Thread
from ..utils.thread_monitor import thread_exists


class OperationalService:
    gateway_address: str
    session_port: int
    attach_port: int | None = None

    gateway_info: GatewayInfo
    _thread_name = "VimarServiceThread"

    _message_handler: MessageHandler
    _error_handler: ErrorHandler
    _keep_alive_handler: KeepAliveHandler
    _web_socket: WSAttachPhase = None
    _send_method: Callable[[BaseRequestResponse], None]

    _waiting_timer: Timer = None
    _user_repo = Database.instance().user_repo

    def __init__(self, gateway_info: GatewayInfo) -> None:
        """Initialize Vimar intagration."""
        self.gateway_address = gateway_info.address
        self.session_port = gateway_info.port
        self.gateway_info = gateway_info
        self._message_handler = MessageHandler(gateway_info)
        self._error_handler = ErrorHandler(gateway_info)
        self._keep_alive_handler = KeepAliveHandler()
        self._waiting_timer = None

    def connect(self):
        """Create a new thread for Operational Phase interaction."""
        thread = Thread(
            target=self._connect,
            name=self._thread_name,
            daemon=True,
        )
        thread.start()
        
    def _connect(self):
        """Handle the connection Vimar WebSocket connection."""
        try:
            self.clean()
            self.sync_session_phase()
            self.async_attach_phase()
        except Exception as err:
            raise VimarErrorResponseException(err) from err

    def send(self):
        self._web_socket.send(None)
        # self._send_method()

    def sync_session_phase(self):
        """Handle SessionPhase interaction."""
        log_info(__name__, "Starting Session Phase...")
        config = self._get_config()
        handler = self._message_handler
        client = SyncSessionPhase(config, handler)
        self.attach_port = client.connect()
        log_info(__name__, "Session Phase Done!")


    def async_attach_phase(self):
        """Handle AttachPhase interaction."""
        log_info(__name__, "Starting Attach Phase...")
        config = self._get_config_for_attach_phase()
        client = WSAttachPhase(config)
        self._web_socket = client.connect()

    def clean(self):
        self.attach_port = None
        self._message_handler.clean()

    def on_attach_connection_opened(
        self, send_method: Callable[[BaseRequestResponse], None]
    ):
        self._send_method = send_method
        self._keep_alive_handler.set_handler(self.send_keep_alive)

    def on_attach_message_received(
        self, message: BaseRequestResponse
    ) -> BaseRequestResponse:
        response = self._message_handler.message_received(message)
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
        if isinstance(message, BaseRequest):
            self.attach_port = None
            self._keep_alive_handler.stop()
            seconds_to_wait = self._get_seconds_to_wait(message)
            message = f"Waiting {str(seconds_to_wait)} seconds before reconnecting..."
            log_info(__name__, message,)
            time.sleep(seconds_to_wait)
            self.connect()

    def handle_keep_alive(self, message: BaseRequestResponse):
        if message:
            self._keep_alive_handler.reset()

    def send_keep_alive(self):
        keep_alive_request = BaseRequest(function="keepalive")
        response = self.on_attach_message_received(keep_alive_request)
        try:
            self._send_method(response)
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
        self._error_handler.remove_database()
