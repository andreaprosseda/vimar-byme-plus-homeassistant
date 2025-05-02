from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.sf_discovery_request import SfDiscoveryRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class AmbientDiscoveryMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_info(
            __name__,
            "Ambient Discovery Phase completed, sending SF Discovery Request...",
        )
        self.save_ambients(message)
        return self.get_sf_discovery_request(config)

    def get_sf_discovery_request(
        self, config: MessageSupportingValues
    ) -> SfDiscoveryRequest:
        return SfDiscoveryRequest(
            target=config.target,
            token=config.token,
            ambient_ids=self.get_all_ambient_ids(),
        )
