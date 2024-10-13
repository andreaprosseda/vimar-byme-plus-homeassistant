from abc import ABC, abstractmethod
from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_request import BaseRequest
from ...model.web_socket.supporting_models.message_supporting_values import MessageSupportingValues

class HandlerInterface(ABC):
    
    @abstractmethod
    def handle_message(self, message: BaseRequestResponse, config: MessageSupportingValues) -> BaseRequestResponse:
        pass
    
    def _idle(self) -> BaseRequestResponse:
        print("Entering idle state: no action required for this phase...")
        return None
    
    def requires_response(self, message: BaseRequest) -> bool:
        return message.params[0]['requiredresp']