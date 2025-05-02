from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from ..base_handler_message import BaseMessageHandler


class RegisterMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        return self._idle()
