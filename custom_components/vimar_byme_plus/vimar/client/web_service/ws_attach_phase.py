from websocket._app import WebSocketApp

from ...model.web_socket.base_request_response import BaseRequestResponse
from ...model.web_socket.base_response import BaseResponse
from ...model.web_socket.web_socket_config import WebSocketConfig
from ...utils.logger import log_error
from .ws_base_vimar import WebSocketBaseVimar


class WSAttachPhase(WebSocketBaseVimar):
    """Attach-phase WebSocket wrapper.

    The four `on_*` callbacks are invoked from the websocket-client
    daemon thread (`run_forever`). Any uncaught exception there bubbles
    up and tears the thread down, leaving the integration silently
    disconnected. Each callback below catches and logs Exception so a
    single buggy handler can't kill the whole connection.
    """

    _config: WebSocketConfig

    def __init__(self, config: WebSocketConfig):
        super().__init__(address=config.address, port=config.port)
        self._config = config

    def on_open(self, ws: WebSocketApp):
        try:
            if self._config.on_open_callback:
                self._config.on_open_callback()
            session_response = self.get_mock_session_response()
            self.on_message(ws, message=session_response)
        except Exception as exc:  # pylint: disable=broad-except
            log_error(__name__, f"on_open raised: {exc!r}")

    def on_close(self, ws: WebSocketApp):
        try:
            callback = self._config.on_close_callback
            if callback:
                callback(self.last_server_message)
        except Exception as exc:  # pylint: disable=broad-except
            log_error(__name__, f"on_close raised: {exc!r}")

    def on_message(self, ws: WebSocketApp, message: BaseRequestResponse):
        try:
            callback = self._config.on_message_callback
            if callback:
                request = callback(message)
                if message.function == "expire":
                    ws.close()
                if request:
                    self.send(request)
        except Exception as exc:  # pylint: disable=broad-except
            log_error(__name__, f"on_message raised: {exc!r}")

    def on_error(self, ws: WebSocketApp, exception: Exception):
        try:
            callback = self._config.on_error_message_callback
            if callback:
                request = callback(
                    self.last_client_message, self.last_server_message, exception
                )
                if request:
                    self.send(request)
                else:
                    ws.close()
        except Exception as exc:  # pylint: disable=broad-except
            log_error(__name__, f"on_error raised: {exc!r}")

    def get_mock_session_response(self) -> BaseResponse:
        return BaseResponse(function="session", msgid=0)

    def close(self):
        self._ws.close()
