from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.response.expire_response import ExpireResponse
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class ExpireMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_info(__name__, "Expire Request received, trying to reconnect...")

        if not self.requires_response(message):
            return self._idle()
        return self.get_expire_response(config)

    def get_expire_response(self, config: MessageSupportingValues) -> ExpireResponse:
        return ExpireResponse(
            target=config.target, token=config.token, msgid=config.msgid
        )
