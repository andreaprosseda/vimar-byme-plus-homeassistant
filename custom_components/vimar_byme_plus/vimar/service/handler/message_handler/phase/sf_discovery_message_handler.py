from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.register_request import RegisterRequest
from .....model.web_socket.request.sf_discovery_request import SfDiscoveryRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_message_handler import BaseMessageHandler


class SfDiscoveryMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        self.add_components(message)

        if config.sfcategory:
            log_info(
                __name__,
                f"SF Discovery Phase done for one category, "
                f"asking for '{config.sfcategory}'...",
            )
            return self.get_sf_discovery_request(config)

        log_info(__name__, "SF Discovery Phase completed, sending Register Request...")
        return self.get_register_request(config)

    def get_sf_discovery_request(
        self, config: MessageSupportingValues
    ) -> SfDiscoveryRequest:
        return SfDiscoveryRequest(
            target=config.target,
            token=config.token,
            ambient_ids=self.get_all_ambient_ids(),
            sfcategory=config.sfcategory,
        )

    def get_register_request(self, config: MessageSupportingValues) -> RegisterRequest:
        return RegisterRequest(
            target=config.target,
            token=config.token,
            components=self.get_all_components(),
        )
