from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.detach_request import DetachRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from ..base_handler_message import BaseMessageHandler


class DetachMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        if not message:
            return self.get_detach_request(config)
        return self._idle()

    def get_detach_request(self, config: MessageSupportingValues) -> DetachRequest:
        return DetachRequest(
            target=config.target, token=config.token, msgid=config.msgid
        )
