"""Manage Web Socket Session Phase."""

from ...model.enum.error_response_enum import ErrorResponse
from ...model.exceptions import VimarErrorResponseException
from ...model.web_socket.base_request import BaseRequest
from ...model.web_socket.base_response import BaseResponse
from .sync_base_socket import SyncBaseSocket


class SyncAttachPhase(SyncBaseSocket):
    """Web Socket Session Phase Class."""

    def connect(self) -> None:
        """Connect with WebSocket."""
        handler = self._handler

        attach_req = handler.start_attach_phase()
        attach_res = self.send_and_wait_for_response(attach_req)

        ambient_discovery_req = handler.message_received(attach_res)
        ambient_discovery_res = self.send_and_wait_for_response(ambient_discovery_req)

        sf_discovery_req = handler.message_received(ambient_discovery_res)
        sf_discovery_res = self.send_and_wait_for_response(sf_discovery_req)

        handler.message_received(sf_discovery_res)
        detach_req = handler.start_detach()
        self.send_and_wait_for_response(detach_req)

        self.close()
        return attach_res

    def send_and_wait_for_response(self, request: BaseRequest) -> BaseResponse:
        """Send a request and wait for response."""
        self.send(request)
        response = self.receive()
        self.check_vimar_error(response)
        return response

    def check_vimar_error(self, response: BaseResponse):
        """Check Vimar Error in response to raise an error."""
        code = response.error if response and response.error else None
        error = ErrorResponse.get_name_by_code(code)
        if error:
            raise VimarErrorResponseException(error)
