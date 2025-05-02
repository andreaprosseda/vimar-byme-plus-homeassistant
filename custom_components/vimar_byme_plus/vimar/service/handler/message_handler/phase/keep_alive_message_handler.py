from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.keep_alive_request import KeepAliveRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class KeepAliveMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        if not message:
            return self.send_keep_alive_request(config)
        return self.handle_keep_alive_response()

    def send_keep_alive_request(
        self, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_info(
            __name__, "Handler requested to send KeepAlive, sending KeepAliveRequest..."
        )
        return self.get_keep_alive_request(config)

    def get_keep_alive_request(
        self, config: MessageSupportingValues
    ) -> KeepAliveRequest:
        return KeepAliveRequest(
            target=config.target, token=config.token, msgid=config.msgid
        )

    def handle_keep_alive_response(self) -> BaseRequestResponse:
        return self._idle()
