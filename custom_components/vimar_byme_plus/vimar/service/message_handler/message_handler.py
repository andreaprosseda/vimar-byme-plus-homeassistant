from ...model.enum.integration_phase import IntegrationPhase
from ...model.gateway.gateway_info import GatewayInfo
from ...model.web_socket.base_request import BaseRequest
from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_response import BaseResponse
from ...model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from ...utils.session_token import get_session_token
from .handler.ambient_discovery_message_handler import AmbientDiscoveryMessageHandler
from .handler.attach_message_handler import AttachMessageHandler
from .handler.change_status_message_handler import ChangeStatusMessageHandler
from .handler.detach_message_handler import DetachMessageHandler
from .handler.expire_message_handler import ExpireMessageHandler
from .handler.keep_alive_message_handler import KeepAliveMessageHandler
from .handler.register_message_handler import RegisterMessageHandler
from .handler.session_message_handler import SessionMessageHandler
from .handler.sf_discovery_message_handler import SfDiscoveryMessageHandler
from .handler.unknown_message_handler import UnknownMessageHandler
from .handler_interface import HandlerInterface


class MessageHandler:
    _gateway_info: GatewayInfo
    _last_msgid: int
    _token: str

    def __init__(self, gateway_info: GatewayInfo):
        self._gateway_info = gateway_info
        self._last_msgid = -1
        self._token = get_session_token()

    def message_received(self, message: BaseRequestResponse) -> BaseRequest:
        phase = self.get_phase(message)
        self.save_msgid_if_needed(message)
        self.save_token_if_needed(phase, message)
        config = self.get_supporting_config()
        handler = MessageHandler.get_handler(phase)
        return handler.handle_message(message, config)

    def get_phase(self, message: BaseRequestResponse) -> IntegrationPhase:
        return IntegrationPhase.get(message.function)

    def save_msgid_if_needed(self, message: BaseRequestResponse):
        if message.msgid:
            self._last_msgid = int(message.msgid)

    def save_token_if_needed(
        self, phase: IntegrationPhase, message: BaseRequestResponse
    ):
        if phase == IntegrationPhase.ATTACH and isinstance(message, BaseResponse):
            self._token = message.result[0]["token"]

    def get_supporting_config(self) -> MessageSupportingValues:
        return MessageSupportingValues(
            target=self._gateway_info.deviceuid,
            token=self._token,
            msgid=self._last_msgid + 1,
            protocol_version=self._gateway_info.protocolversion,
        )

    @staticmethod
    def get_handler(phase: IntegrationPhase) -> HandlerInterface:
        match phase:
            case IntegrationPhase.SESSION:
                return SessionMessageHandler()
            case IntegrationPhase.ATTACH:
                return AttachMessageHandler()
            case IntegrationPhase.AMBIENT_DISCOVERY:
                return AmbientDiscoveryMessageHandler()
            case IntegrationPhase.SF_DISCOVERY:
                return SfDiscoveryMessageHandler()
            case IntegrationPhase.CHANGE_STATUS:
                return ChangeStatusMessageHandler()
            case IntegrationPhase.EXPIRE:
                return ExpireMessageHandler()
            case IntegrationPhase.REGISTER:
                return RegisterMessageHandler()
            case IntegrationPhase.KEEP_ALIVE:
                return KeepAliveMessageHandler()
            case IntegrationPhase.DETACH:
                return DetachMessageHandler()
            case _:
                return UnknownMessageHandler()
