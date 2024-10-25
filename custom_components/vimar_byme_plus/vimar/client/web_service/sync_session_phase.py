"""Manage Web Socket Session Phase."""

from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_response import BaseResponse
from .sync_base_socket import SyncBaseSocket


class SyncSessionPhase(SyncBaseSocket):
    """Web Socket Session Phase Class."""

    def connect(self) -> int:
        """Connect with WebSocket."""
        request = self._handler.start_session_phase()
        self.send(request)
        response = self.receive()
        self.close()
        return self._get_port_to_attach(response)

    def _get_port_to_attach(self, response: BaseRequestResponse) -> int:
        """Return port for AttachPhase."""
        if isinstance(response, BaseResponse):
            return response.result[0]["communication"]["ipport"]
        return -1
