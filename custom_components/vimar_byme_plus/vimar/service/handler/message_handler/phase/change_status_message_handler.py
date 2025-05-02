from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.response.changestatus_response import ChangeStatusResponse
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_debug
from ..base_handler_message import BaseMessageHandler


class ChangeStatusMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_debug(__name__, "Change Status received, saving content...")
        self.save_component_changes(message)

        if not self.requires_response(message):
            return self._idle()
        return self.get_change_status_response(config)

    def get_change_status_response(
        self, config: MessageSupportingValues
    ) -> ChangeStatusResponse:
        return ChangeStatusResponse(
            target=config.target, token=config.token, msgid=config.msgid
        )
