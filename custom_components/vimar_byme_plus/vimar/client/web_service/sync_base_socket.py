"""Manage Web Socket Session Phase."""

import json
import ssl
from typing import Any

from websocket import WebSocket, create_connection

from ...model.web_socket.base_request import BaseRequest
from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_response import BaseResponse
from ...model.web_socket.request.session_request import SessionRequest
from ...model.web_socket.web_socket_config import WebSocketConfig
from ...service.handler.message_handler.message_handler import MessageHandler
from ...utils.logger import log_debug, log_info
from ...utils.session_token import get_session_token


class SyncBaseSocket:
    """Web Socket Session Phase Class."""

    ws: WebSocket = None
    _config: WebSocketConfig
    _handler: MessageHandler

    def __init__(self, config: WebSocketConfig, handler: MessageHandler) -> None:
        """Initialize WebSocket Session Phase."""
        self._config = config
        self._handler = handler
        url = f"wss://{self._config.address}:{self._config.port}"
        self.ws = self._create_connection(url)

    def connect(self) -> Any:
        """Connect with WebSocket."""
        return None

    def _create_connection(self, url: str) -> WebSocket:
        """Create WebSocket connection."""
        log_info(__name__, f"Connecting to {url}...")
        ssl_opt = self._get_ssl_options()
        return create_connection(url, sslopt=ssl_opt)

    def send(self, message: BaseRequestResponse):
        """Send BaseRequestResponse object."""
        json_string = message.to_json()
        log_debug(__name__, f"Sending message:\n{json_string}")
        self.ws.send(json_string)

    def receive(self) -> BaseRequestResponse:
        """Receive message."""
        log_debug(__name__, "Waiting for response...")
        message = self.ws.recv()
        log_debug(__name__, f"Received message:\n{message}")
        return self._get_object(message)

    def close(self):
        """Close the WebSocket connection."""
        self.ws.close()

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

    def _get_object(self, message: str) -> BaseRequestResponse:
        json_message = json.loads(message)
        if json_message["type"] == "request":
            return BaseRequest(**json_message)
        if json_message["type"] == "response":
            return BaseResponse(**json_message)
        raise ValueError(f"Unknown message type: {json_message['type']}")
