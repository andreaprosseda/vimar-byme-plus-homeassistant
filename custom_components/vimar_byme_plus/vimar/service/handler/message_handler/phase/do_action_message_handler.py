from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.doaction_request import DoActionRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class DoActionMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        if not message and config.actions:
            return self.get_do_action_request(config)
        return self._idle()

    def get_do_action_request(self, config: MessageSupportingValues) -> DoActionRequest:
        log_info(
            __name__, "Handler requested to send DoAction, sending DoActionRequest..."
        )
        return DoActionRequest(
            target=config.target,
            token=config.token,
            msgid=config.msgid,
            actions=config.actions,
        )
