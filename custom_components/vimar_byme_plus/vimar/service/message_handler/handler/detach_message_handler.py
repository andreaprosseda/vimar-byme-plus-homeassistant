from ....model.web_socket.base_request_response import BaseRequestResponse
from ..base_handler_message import BaseMessageHandler
from ....model.web_socket.supporting_models.message_supporting_values import MessageSupportingValues

class DetachMessageHandler(BaseMessageHandler):
    
    def handle_message(self, message: BaseRequestResponse, config: MessageSupportingValues) -> BaseRequestResponse:
        return self._idle()