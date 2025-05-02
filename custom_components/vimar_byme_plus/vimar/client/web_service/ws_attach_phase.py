from websocket._app import WebSocketApp

from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_response import BaseResponse
from ...model.web_socket.web_socket_config import WebSocketConfig
from .ws_base_vimar import WebSocketBaseVimar


class WSAttachPhase(WebSocketBaseVimar):
    _config: WebSocketConfig

    def __init__(self, config: WebSocketConfig):
        super().__init__(address=config.address, port=config.port)
        self._config = config

    def on_open(self, ws: WebSocketApp):
        if self._config.on_open_callback:
            self._config.on_open_callback()

        session_response = self.get_mock_session_response()
        self.on_message(ws, message=session_response)

    def on_close(self, ws: WebSocketApp):
        callback = self._config.on_close_callback
        if callback:
            callback(self.last_server_message)

    def on_message(self, ws: WebSocketApp, message: BaseRequestResponse):
        callback = self._config.on_message_callback
        if callback:
            request = callback(message)
            if message.function == "expire":
                ws.close()
            if request:
                self.send(request)

    def on_error(self, ws: WebSocketApp, exception: Exception):
        callback = self._config.on_error_message_callback
        if callback:
            request = callback(
                self.last_client_message, self.last_server_message, exception
            )
            if request:
                self.send(request)
            else:
                ws.close()

    def get_mock_session_response(self) -> BaseResponse:
        return BaseResponse(function="session", msgid=0)

    def close(self):
        self._ws.close()
