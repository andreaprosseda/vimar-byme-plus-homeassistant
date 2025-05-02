from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.detach_request import DetachRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_error
from ..base_handler_message import BaseMessageHandler


class UnknownMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_error(__name__, "Unknown Phase!!!")
        return self.get_detach_request(config)

    def get_detach_request(self, config: MessageSupportingValues) -> DetachRequest:
        return DetachRequest(
            target=config.target, token=config.token, msgid=config.msgid
        )
