from ....model.web_socket.base_request_response import BaseRequestResponse
from ..base_handler_message import BaseMessageHandler
from ....model.web_socket.request.attach_request import AttachRequest
from ....model.web_socket.supporting_models.message_supporting_values import MessageSupportingValues

class SessionMessageHandler(BaseMessageHandler):
    
    def handle_message(self, message: BaseRequestResponse, config: MessageSupportingValues) -> BaseRequestResponse:
        print('Session phase completed, sending Attach Request...')
        return self.get_attach_request(config)
    
    def get_attach_request(self, config: MessageSupportingValues) -> AttachRequest:
        return AttachRequest(
            target=config.target,
            token=config.token,
            protocol_version=config.protocol_version,
            user_credentials=self.get_user_credentials()
        )
