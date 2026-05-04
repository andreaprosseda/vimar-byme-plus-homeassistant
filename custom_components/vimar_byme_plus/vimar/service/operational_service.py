from collections.abc import Coroutine
import time
from typing import Any

from websocket import WebSocketConnectionClosedException

from ..client.web_service.sync_session_phase import SyncSessionPhase
from ..client.web_service.ws_attach_phase import WSAttachPhase
from ..database.database import Database, set_current_gateway_uid
from ..model.component.vimar_component import VimarComponent
from ..model.enum.action_type import ActionType
from ..model.enum.integration_phase import IntegrationPhase
from ..model.exceptions import VimarErrorResponseException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.web_socket.base_request import BaseRequest
from ..model.web_socket.base_request_response import BaseRequestResponse
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..scheduler.keep_alive_handler import KeepAliveHandler
from ..utils.logger import log_info, log_debug
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
    _component_repo = Database.instance().component_repo
    _ambient_repo = Database.instance().ambient_repo
    _bootstrapped: bool = False

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
        # Tag this thread with the active gateway so any handler invoked
        # from the WS callbacks can scope DB queries correctly.
        set_current_gateway_uid(self.gateway_info.deviceuid)
        # One-shot migration: rows that pre-date the multi-gateway scoping
        # have gateway_uid = NULL. Claim them for whichever gateway connects
        # first. Only safe when the fork was previously single-gateway, but
        # that's exactly the case we're upgrading from.
        self._claim_legacy_rows()
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

    def _claim_legacy_rows(self) -> None:
        """Migrate pre-multi-gateway rows (gateway_uid IS NULL) to this gateway."""
        uid = self.gateway_info.deviceuid
        log_info(__name__, f"Attempting to claim legacy rows for {uid}")
        # Use repo's own execute to keep transactions consistent
        for repo, table in (
            (self._user_repo, "users"),
            (self._component_repo, "components"),
            (self._ambient_repo, "ambients"),
        ):
            try:
                repo.execute(
                    f"UPDATE {table} SET gateway_uid = ? WHERE gateway_uid IS NULL",
                    (uid,),
                )
            except Exception as exc:  # noqa: BLE001
                log_info(__name__, f"Claim {table} failed: {exc}")
        # element_repo: it's a sub-repo of component_repo, exposed via that one
        try:
            self._component_repo.element_repo.execute(
                "UPDATE elements SET gateway_uid = ? WHERE gateway_uid IS NULL",
                (uid,),
            )
        except Exception as exc:  # noqa: BLE001
            log_info(__name__, f"Claim elements failed: {exc}")

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
        log_debug(__name__, message)
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
        # Re-tag thread (defensive: callbacks may run on a separate thread).
        set_current_gateway_uid(self.gateway_info.deviceuid)
        # TEMP DIAG: re-enabled to validate Bug #4 bootstrap
        try:
            import time as _t
            with open("/config/vimar_ws_dump.log", "a", encoding="utf-8") as _f:
                _f.write(
                    f"--- {_t.strftime('%H:%M:%S')} gw={self.gateway_info.deviceuid} "
                    f"type={type(message).__name__} "
                    f"function={getattr(message, 'function', '?')} "
                    f"msgid={getattr(message, 'msgid', '?')} ---\n"
                )
                try:
                    _f.write(message.to_json() + "\n")
                except Exception:
                    _f.write(repr(message) + "\n")
        except Exception:
            pass
        response = self._message_handler.message_received(message)
        self.trigger_changes(message)
        self.handle_keep_alive(response)
        self._maybe_bootstrap_states(message)
        return response

    def _maybe_bootstrap_states(self, message: BaseRequestResponse) -> None:
        """Request initial state of every component once after sfdiscovery.

        Vimar gateways only push `changestatus` events when a value actually
        changes. Devices that haven't moved since startup (lights left off,
        thermostats at setpoint, shutters fully open or closed) never reach
        HA, so their entities remain `unknown`/`off` until the user touches
        them. Right after `sfdiscovery` the database has the full component
        list, so we can ask the gateway for the current state of each idsf
        once and let the normal change-status flow keep them in sync from
        there.
        """
        if self._bootstrapped:
            return
        if isinstance(message, BaseRequest):
            return  # only react to gateway responses
        phase = IntegrationPhase.get(getattr(message, "function", None))
        if phase != IntegrationPhase.SF_DISCOVERY:
            return
        try:
            components = self._component_repo.get_all(
                gateway_uid=self.gateway_info.deviceuid
            )
        except Exception as exc:  # noqa: BLE001
            log_info(__name__, f"Bootstrap states: cannot read components: {exc}")
            return
        if not components:
            return
        log_info(
            __name__,
            f"Bootstrap states: requesting status of {len(components)} components",
        )
        for component in components:
            try:
                self.send_get_status(component.idsf)
            except Exception as exc:  # noqa: BLE001
                log_info(
                    __name__,
                    f"Bootstrap states: get_status failed for idsf={component.idsf}: {exc}",
                )
        self._bootstrapped = True

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
        config.user_credentials = self._user_repo.get_current_user(
            gateway_uid=self.gateway_info.deviceuid
        )
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
