import json
import ssl
from websocket._app import WebSocketApp
from ...model.web_socket.base_request import BaseRequest
from ...model.enum.error_response_enum import ErrorResponse

class WebSocketBaseVimar:
    
    last_response: str = None

    _url: str
    
    def __init__(self, address: str, port: str):
        self._url = f"wss://{address}:{port}"
        
    def connect(self):
        print(f"Connecting to {self._url}...")
        ssl_opt = self.get_ssl_options()
        ws = self.get_web_socket_app(self._url)
        ws.run_forever(sslopt=ssl_opt)
            
    def get_web_socket_app(self, url) -> WebSocketApp:
        return WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        
    def get_ssl_options(self) -> dict:
        return {
            "cert_reqs": ssl.CERT_NONE,
            # "cert_reqs": ssl.CERT_REQUIRED,
            # "ca_certs": "vimar_connection/data/VimarCA.cert.pem"
        }
    
    def _on_message(self, ws: WebSocketApp, message: str):
        print(f"Received message:\n{message}")
        json_message = json.loads(message)
        if self.is_error(json_message):
            self.on_error(ws, json_message)
        else:
            self.last_response = json_message
            self.on_message(ws, json_message)

    def _on_error(self, ws: WebSocketApp, error: Exception):
        print(f"Error occurred: {error}")
        self.on_error(ws, None)

    def _on_close(self, ws: WebSocketApp, close_status_code: int, close_msg: str):
        print("Connection closed")
        if close_status_code:
            print(f"Status Code: {close_status_code}")
        if close_msg:
            print(f"Close Message: {close_msg}")
        self.on_close(ws)
        
    def _on_open(self, ws: WebSocketApp):
        print("Opening connection...")
        self.on_open(ws)
        
    def is_error(self, response: dict) -> bool:
        error_code = response['error']
        name = ErrorResponse.get_name_by_code(error_code)
        if name:
            print("\n" + name + "\n")
            return True
        return False
        
    def on_message(self, ws: WebSocketApp, message: dict):
        raise NotImplementedError()
            
    def on_error(self, ws: WebSocketApp, message: dict):
        pass
    
    def on_close(self, ws: WebSocketApp):
        pass

    def on_open(self, ws: WebSocketApp):
        raise NotImplementedError()
    
    def send(self, ws: WebSocketApp, request: BaseRequest):
        json_string = request.to_json()
        print(f"Sending message:\n{json_string}")
        ws.send(json_string)