from ....model.component.vimar_action import VimarAction
from ....model.enum.integration_phase import IntegrationPhase
from ....model.gateway.gateway_info import GatewayInfo
from ....model.web_socket.base_request import BaseRequest
from ....model.web_socket.base_request_response import BaseRequestResponse
from ....model.web_socket.base_response import BaseResponse
from ....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from ....utils.session_token import get_session_token
from .base_message_handler import HandlerInterface
from .phase.ambient_discovery_message_handler import AmbientDiscoveryMessageHandler
from .phase.attach_message_handler import AttachMessageHandler
from .phase.change_status_message_handler import ChangeStatusMessageHandler
from .phase.detach_message_handler import DetachMessageHandler
from .phase.do_action_message_handler import DoActionMessageHandler
from .phase.expire_message_handler import ExpireMessageHandler
from .phase.get_status_message_handler import GetStatusMessageHandler
from .phase.init_message_handler import InitMessageHandler
from .phase.keep_alive_message_handler import KeepAliveMessageHandler
from .phase.register_message_handler import RegisterMessageHandler
from .phase.session_message_handler import SessionMessageHandler
from .phase.sf_discovery_message_handler import SfDiscoveryMessageHandler
from .phase.unknown_message_handler import UnknownMessageHandler

# The gateway honours only the FIRST sfcategory of an sfdiscovery
# request and silently ignores the remaining ones, so every category has
# to be asked for in its own request.
SF_CATEGORIES: tuple[str, ...] = ("Plant", "LogicProgram")


class MessageHandler:
    _gateway_info: GatewayInfo
    _gateway_id: str
    _last_msgid: int
    _token: str
    _pending_sf_categories: list[str]

    def __init__(self, gateway_info: GatewayInfo) -> None:
        self._gateway_info = gateway_info
        self._gateway_id = gateway_info.deviceuid
        self._last_msgid = -1
        self._token = get_session_token()
        self._pending_sf_categories = list(SF_CATEGORIES)

    def start_session_phase(self) -> BaseRequest:
        phase = IntegrationPhase.INIT
        return self.message_from_phase(phase)

    def start_attach_phase(self) -> BaseRequest:
        phase = IntegrationPhase.SESSION
        return self.message_from_phase(phase)

    def start_detach(self) -> BaseRequest:
        phase = IntegrationPhase.DETACH
        return self.message_from_phase(phase)

    def start_keep_alive(self) -> BaseRequest:
        phase = IntegrationPhase.KEEP_ALIVE
        return self.message_from_phase(phase)

    def start_do_action(self, actions: list[VimarAction]) -> BaseRequest:
        phase = IntegrationPhase.DO_ACTION
        return self.message_from_phase(phase, actions)

    def start_get_status(self, idsf: int) -> BaseRequest:
        phase = IntegrationPhase.GET_STATUS
        return self.message_from_phase(phase, idsf)

    def message_from_phase(self, phase: IntegrationPhase, *args) -> BaseRequestResponse:
        config = self._get_supporting_config(*args)
        handler = self._get_handler(phase)
        return handler.handle_message(None, config)

    def message_received(self, message: BaseRequestResponse) -> BaseRequestResponse:
        phase = self._get_phase(message)
        self._complete_sf_category_if_needed(phase)
        self._save_msgid_if_needed(message)
        self._save_token_if_needed(phase, message)
        config = self._get_supporting_config()
        handler = self._get_handler(phase)
        return handler.handle_message(message, config)

    def clean(self):
        self._last_msgid = -1
        self._token = get_session_token()
        self._pending_sf_categories = list(SF_CATEGORIES)

    def _get_phase(self, message: BaseRequestResponse) -> IntegrationPhase:
        return IntegrationPhase.get(message.function)

    def _complete_sf_category_if_needed(self, phase: IntegrationPhase):
        """Drop the category whose sfdiscovery response just arrived."""
        if phase == IntegrationPhase.SF_DISCOVERY and self._pending_sf_categories:
            self._pending_sf_categories.pop(0)

    def _next_sf_category(self) -> str | None:
        """Return the category the next sfdiscovery has to ask for."""
        if not self._pending_sf_categories:
            return None
        return self._pending_sf_categories[0]

    def _save_msgid_if_needed(self, message: BaseRequestResponse):
        if message.msgid:
            self._last_msgid = int(message.msgid)

    def _save_token_if_needed(
        self, phase: IntegrationPhase, message: BaseRequestResponse
    ):
        if phase == IntegrationPhase.ATTACH and isinstance(message, BaseResponse):
            self._token = message.result[0]["token"]

    def _get_supporting_config(self, *args) -> MessageSupportingValues:
        return MessageSupportingValues(
            ip_address=self._gateway_info.address,
            target=self._gateway_info.deviceuid,
            token=self._token,
            msgid=self._last_msgid + 1,
            protocol_version=self._gateway_info.protocolversion,
            actions=args[0] if args else [],
            idsf=args[0] if args else [],
            sfcategory=self._next_sf_category(),
        )

    def _get_handler(self, phase: IntegrationPhase) -> HandlerInterface:
        gw = self._gateway_id
        match phase:
            case IntegrationPhase.INIT:
                return InitMessageHandler(gw)
            case IntegrationPhase.SESSION:
                return SessionMessageHandler(gw)
            case IntegrationPhase.ATTACH:
                return AttachMessageHandler(gw)
            case IntegrationPhase.AMBIENT_DISCOVERY:
                return AmbientDiscoveryMessageHandler(gw)
            case IntegrationPhase.SF_DISCOVERY:
                return SfDiscoveryMessageHandler(gw)
            case IntegrationPhase.DO_ACTION:
                return DoActionMessageHandler(gw)
            case IntegrationPhase.CHANGE_STATUS:
                return ChangeStatusMessageHandler(gw)
            case IntegrationPhase.EXPIRE:
                return ExpireMessageHandler(gw)
            case IntegrationPhase.REGISTER:
                return RegisterMessageHandler(gw)
            case IntegrationPhase.GET_STATUS:
                return GetStatusMessageHandler(gw)
            case IntegrationPhase.KEEP_ALIVE:
                return KeepAliveMessageHandler(gw)
            case IntegrationPhase.DETACH:
                return DetachMessageHandler(gw)
            case _:
                return UnknownMessageHandler(gw)
