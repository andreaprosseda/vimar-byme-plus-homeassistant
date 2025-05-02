from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.ambient_discovery_request import (
    AmbientDiscoveryRequest,
)
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class AttachMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        log_info(
            __name__, "Attach Phase completed, sending Ambient Discovery Request..."
        )
        return self.get_ambient_discovery_request(config)

    def get_ambient_discovery_request(
        self, config: MessageSupportingValues
    ) -> AmbientDiscoveryRequest:
        return AmbientDiscoveryRequest(target=config.target, token=config.token)
