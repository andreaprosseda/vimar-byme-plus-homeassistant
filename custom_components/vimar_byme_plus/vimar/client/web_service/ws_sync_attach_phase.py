"""Manage Web Socket Session Phase."""

import json
import ssl

from websocket import WebSocket, create_connection

from ...model.web_socket.base_response import BaseResponse
from ...model.web_socket.request.session_request import SessionRequest
from ...model.web_socket.web_socket_config import WebSocketConfig
from ...utils.logger import log_debug, log_info
from ...utils.session_token import get_session_token


class WSSessionPhase:
    """Web Socket Session Phase Class."""

    _config: WebSocketConfig

    def __init__(self, config: WebSocketConfig) -> None:
        """Initialize WebSocket Session Phase."""
        self._config = config

    def connect(self) -> int:
        """Connect with WebSocket."""
        url = f"wss://{self._config.address}:{self._config.port}"
        ws = self._create_connection(url)
        self._send_session_request(ws)
        response = self._receive_session_response(ws)
        self._close_connection(ws)
        return response

    def _create_connection(self, url: str) -> WebSocket:
        """Create WebSocket connection."""
        log_info(__name__, f"Connecting to {url}...")
        ssl_opt = self._get_ssl_options()
        return create_connection(url, sslopt=ssl_opt)

    def _send_session_request(self, ws: WebSocket):
        """Send SessionRequest object."""
        request = self._get_session_request()
        json_string = request.to_json()
        log_debug(__name__, f"Sending message:\n{json_string}")
        ws.send(json_string)

    def _receive_session_response(self, ws: WebSocket) -> int:
        """Receive SessionResponse object."""
        log_debug(__name__, "Receiving SessionResponse...")
        message = ws.recv()
        log_debug(__name__, f"Received message:\n{message}")
        return self._get_port_to_attach(message)

    def _close_connection(self, ws: WebSocket):
        """Close the WebSocket connection."""
        ws.close()

    def _get_ssl_options(self) -> dict:
        """Return SSL Options for WSS Connection."""
        return {
            "cert_reqs": ssl.CERT_NONE,
        }
        # "cert_reqs": ssl.CERT_REQUIRED,
        # "ca_certs": "vimar/data/VimarCA.cert.pem"

    def _get_session_request(self) -> SessionRequest:
        """Create SessionRequest from _config."""
        target = self._config.gateway_info.deviceuid
        return SessionRequest(target=target, token=get_session_token())

    def _get_port_to_attach(self, message: str) -> int:
        """Return port for AttachPhase."""
        json_message = json.loads(message)
        response = BaseResponse(**json_message)
        return response.result[0]["communication"]["ipport"]
