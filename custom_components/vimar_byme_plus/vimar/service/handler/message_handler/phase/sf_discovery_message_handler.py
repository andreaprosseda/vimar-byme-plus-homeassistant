from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.register_request import RegisterRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class SfDiscoveryMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_info(__name__, "SF Discovery Phase completed, sending Register Request...")
        self.save_components(message)
        return self.get_register_request(config)

    def get_register_request(self, config: MessageSupportingValues) -> RegisterRequest:
        return RegisterRequest(
            target=config.target,
            token=config.token,
            components=self.get_all_components(),
        )
