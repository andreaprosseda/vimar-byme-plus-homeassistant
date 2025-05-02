from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.attach_request import AttachRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_debug
from ..base_handler_message import BaseMessageHandler


class SessionMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_debug(__name__, "Session phase completed, sending Attach Request...")
        return self.get_attach_request(config)

    def get_attach_request(self, config: MessageSupportingValues) -> AttachRequest:
        return AttachRequest(
            target=config.target,
            token=config.token,
            protocol_version=config.protocol_version,
            user_credentials=self.get_user_credentials(),
            ip_address=config.ip_address,
        )
