from .ws_base_vimar import WebSocketBaseVimar
from websocket._app import WebSocketApp
from ..model.web_socket.base_request_response import BaseRequestResponse
from ..model.web_socket.request.session_request import SessionRequest
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..utils.session_token import get_session_token

class WSSessionPhase(WebSocketBaseVimar):
    
    _config: WebSocketConfig
    
    def __init__(self, config: WebSocketConfig):
        super().__init__(address=config.address,port=config.port)
        self._config = config
    
    def on_open(self, ws: WebSocketApp):
        request = self.get_session_request()
        self.send(request)

    def on_message(self, ws: WebSocketApp, message: BaseRequestResponse):
        ws.close()

    def on_close(self, ws: WebSocketApp):
        callback = self._config.on_close_callback
        if callback:
            callback(self.last_response)

    def get_session_request(self) -> SessionRequest:
        return SessionRequest(
            target=self._config.gateway_info.deviceuid,
            token=get_session_token()
        )