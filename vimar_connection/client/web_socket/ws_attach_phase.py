from .ws_base_vimar import WebSocketBaseVimar
from websocket._app import WebSocketApp
from ...model.web_socket.web_socket_config import WebSocketConfig

class WSAttachPhase(WebSocketBaseVimar):
    
    _config: WebSocketConfig
    
    def __init__(self, config: WebSocketConfig):
        super().__init__(address=config.address,port=config.port)
        self._config = config
    
    def on_open(self, ws: WebSocketApp):
        callback = self._config.on_open_callback
        if callback:
            callback(self.send)
        
        self.on_message(ws, message={'function' : 'session', 'msgid' : 0})
        # request = self.get_attach_request()
        # self.send(request)

    def on_close(self, ws: WebSocketApp):
        callback = self._config.on_close_callback
        if callback:
            callback(self.last_response)
    
    def on_message(self, ws: WebSocketApp, message: dict):
        callback = self._config.on_message_callback
        if callback:
            request = callback(message)
            if request:
                self.send(request)

    def on_error(self, ws: WebSocketApp, message: dict):
        callback = self._config.on_error_message_callback
        if callback:
            request = callback(message)
            if request:
                self.send(request)