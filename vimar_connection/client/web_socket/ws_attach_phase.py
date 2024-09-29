from .ws_base_vimar import WebSocketBaseVimar
from websocket._app import WebSocketApp
from ...model.web_socket.attach_request import AttachRequest
from ...model.web_socket.web_socket_config import WebSocketConfig

class WSAttachPhase(WebSocketBaseVimar):
    
    _config: WebSocketConfig
    
    def __init__(self, config: WebSocketConfig):
        super().__init__(address=config.address,port=config.port)
        self._config = config
    
    def on_open(self, ws: WebSocketApp):
        self.on_message(ws, message={'function' : 'session'})
        # request = self.get_attach_request()
        # self.send(ws, request)

    def on_message(self, ws: WebSocketApp, message: dict):
        callback = self._config.on_message_callback
        if callback:
            request = callback(message)
            if request:
                self.send(ws, request)

    def on_error(self, ws: WebSocketApp, message: dict):
        callback = self._config.on_error_message_callback
        if callback:
            request = callback(message)
            if request:
                self.send(ws, request)
    
    # def get_attach_request(self) -> AttachRequest:
    #     return AttachRequest(
    #         target=self._config.gateway_info.deviceuid,
    #         token=self.
    #         protocol_version=self._config.gateway_info.protocolversion,
    #         user_credentials=self._config.user_credentials
    #     )