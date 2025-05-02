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
from .base_handler_message import HandlerInterface
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


class MessageHandler:
    _gateway_info: GatewayInfo
    _last_msgid: int
    _token: str

    def __init__(self, gateway_info: GatewayInfo) -> None:
        self._gateway_info = gateway_info
        self._last_msgid = -1
        self._token = get_session_token()

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
        handler = MessageHandler._get_handler(phase)
        return handler.handle_message(None, config)

    def message_received(self, message: BaseRequestResponse) -> BaseRequestResponse:
        phase = self._get_phase(message)
        self._save_msgid_if_needed(message)
        self._save_token_if_needed(phase, message)
        config = self._get_supporting_config()
        handler = MessageHandler._get_handler(phase)
        return handler.handle_message(message, config)

    def clean(self):
        self._last_msgid = -1
        self._token = get_session_token()

    def _get_phase(self, message: BaseRequestResponse) -> IntegrationPhase:
        return IntegrationPhase.get(message.function)

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
        )

    @staticmethod
    def _get_handler(phase: IntegrationPhase) -> HandlerInterface:
        match phase:
            case IntegrationPhase.INIT:
                return InitMessageHandler()
            case IntegrationPhase.SESSION:
                return SessionMessageHandler()
            case IntegrationPhase.ATTACH:
                return AttachMessageHandler()
            case IntegrationPhase.AMBIENT_DISCOVERY:
                return AmbientDiscoveryMessageHandler()
            case IntegrationPhase.SF_DISCOVERY:
                return SfDiscoveryMessageHandler()
            case IntegrationPhase.DO_ACTION:
                return DoActionMessageHandler()
            case IntegrationPhase.CHANGE_STATUS:
                return ChangeStatusMessageHandler()
            case IntegrationPhase.EXPIRE:
                return ExpireMessageHandler()
            case IntegrationPhase.REGISTER:
                return RegisterMessageHandler()
            case IntegrationPhase.GET_STATUS:
                return GetStatusMessageHandler()
            case IntegrationPhase.KEEP_ALIVE:
                return KeepAliveMessageHandler()
            case IntegrationPhase.DETACH:
                return DetachMessageHandler()
            case _:
                return UnknownMessageHandler()
