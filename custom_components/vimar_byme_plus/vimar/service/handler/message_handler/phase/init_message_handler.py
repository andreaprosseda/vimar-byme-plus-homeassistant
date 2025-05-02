from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.session_request import SessionRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_debug
from .....utils.session_token import get_session_token
from ..base_handler_message import BaseMessageHandler


class InitMessageHandler(BaseMessageHandler):
    """Manage Init Handler."""

    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        """Handle Initialization for Session Phase."""
        log_debug(__name__, "Session phase completed, sending Attach Request...")
        return self.get_session_request(config)

    def get_session_request(self, config: MessageSupportingValues) -> SessionRequest:
        """Return SessionRequest object."""
        return SessionRequest(
            target=config.target,
            token=get_session_token(),
            ip_address=config.ip_address,
        )
