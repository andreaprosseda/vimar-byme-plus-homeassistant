import json
import ssl
import traceback

from websocket import WebSocketApp

from ...model.enum.error_response_enum import ErrorResponse
from ...model.web_socket.base_request import BaseRequest
from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_response import BaseResponse
from ...utils.logger import log_debug, log_error, log_info


class WebSocketBaseVimar:
    last_client_message: BaseRequestResponse = None
    last_server_message: BaseRequestResponse = None
    _url: str
    _ws: WebSocketApp

    def __init__(self, address: str, port: str):
        self._url = f"wss://{address}:{port}"

    def connect(self):
        log_info(__name__, f"Connecting to {self._url}...")
        ssl_opt = self.get_ssl_options()
        self._ws = self.get_web_socket_app(self._url)
        self._ws.run_forever(sslopt=ssl_opt)

    def get_web_socket_app(self, url) -> WebSocketApp:
        return WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

    def get_ssl_options(self) -> dict:
        return {
            "cert_reqs": ssl.CERT_NONE,
            # "cert_reqs": ssl.CERT_REQUIRED,
            # "ca_certs": "vimar/data/VimarCA.cert.pem"
        }

    def _on_message(self, ws: WebSocketApp, message: str):
        log_debug(__name__, f"Received message:\n{message}")
        message_object = self.get_object(message)
        self.last_server_message = message_object
        if self.is_error(message_object):
            self.on_error(ws, None)
        else:
            self.on_message(ws, message_object)

    def _on_error(self, ws: WebSocketApp, error: Exception):
        error_type = type(error).__name__
        log_error(__name__, f"Error occurred: {error_type}: {error!s}")
        log_error(__name__, f"Stack trace:\n{traceback.format_exc()}")
        self.on_error(ws, error)

    def _on_close(self, ws: WebSocketApp, close_status_code: int, close_msg: str):
        log_info(__name__, "Connection closed")
        if close_status_code:
            log_info(__name__, f"Status Code: {close_status_code}")
        if close_msg:
            log_info(__name__, f"Close Message: {close_msg}")
        self.on_close(ws)

    def _on_open(self, ws: WebSocketApp):
        log_debug(__name__, "Opening connection...")
        self.on_open(ws)

    def is_error(self, base_request_response: BaseRequestResponse) -> bool:
        if isinstance(base_request_response, BaseResponse):
            error_code = base_request_response.error
            name = ErrorResponse.get_name_by_code(error_code)
            if name:
                log_error(__name__, f"\nCurrent error code name is: {name}\n")
                return True
        return False

    def on_message(self, ws: WebSocketApp, message: BaseRequestResponse):
        raise NotImplementedError

    def on_error(self, ws: WebSocketApp, exception: Exception):
        pass

    def on_close(self, ws: WebSocketApp):
        pass

    def on_open(self, ws: WebSocketApp):
        raise NotImplementedError

    def send(self, request: BaseRequestResponse):
        if not request:
            return
        self.last_client_message = request
        json_string = request.to_json()
        log_debug(__name__, f"Sending message:\n{json_string}")
        self._ws.send(json_string)

    def get_object(self, message: str) -> BaseRequestResponse:
        json_message = json.loads(message)
        if json_message["type"] == "request":
            return BaseRequest(**json_message)
        if json_message["type"] == "response":
            return BaseResponse(**json_message)
        raise ValueError(f"Unknown message type: {json_message['type']}")
