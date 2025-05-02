from .....model.web_socket.base_request_response import BaseRequestResponse
from .....model.web_socket.request.getstatus_request import GetStatusRequest
from .....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from .....utils.logger import log_info
from ..base_handler_message import BaseMessageHandler


class GetStatusMessageHandler(BaseMessageHandler):
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        if not message and config.actions:
            return self.get_status_request(config)
        # self.log(message)
        return self._idle()

    def get_status_request(self, config: MessageSupportingValues) -> GetStatusRequest:
        log_info(
            __name__, "Handler requested to send GetStatus, sending GetStatusRequest..."
        )
        return GetStatusRequest(
            target=config.target,
            token=config.token,
            msgid=config.msgid,
            idsf=config.idsf,
        )

    # def log(self, response: BaseRequestResponse):
    #     if response and isinstance(response, BaseResponse):
    #         if response.result:
    #             print_elements(response.result[0]["elements"])
