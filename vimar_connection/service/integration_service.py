import time
from typing import Callable, Optional
from websocket._exceptions import WebSocketConnectionClosedException
from .message_handler.message_handler import MessageHandler
from .error_handler.error_handler import ErrorHandler
from ..client.ws_attach_phase import WSAttachPhase
from ..client.ws_session_phase import WSSessionPhase
from ..database.database import Database
from ..model.gateway.gateway_info import GatewayInfo
from ..model.web_socket.base_request_response import BaseRequestResponse
from ..model.web_socket.base_request import BaseRequest
from ..model.web_socket.base_response import BaseResponse
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..scheduler.keep_alive_handler import KeepAliveHandler
from ..utils.logger import log_info
from ..utils.thread import Timer

class IntegrationService:
    
    gateway_address: str
    session_port: int
    attach_port: Optional[int] = None
    
    _gateway_info: GatewayInfo
    _message_handler: MessageHandler
    _error_handler: ErrorHandler
    _keep_alive_handler: KeepAliveHandler
    _send_method: Callable[[BaseRequestResponse], None]
    
    _waiting_timer: Timer = None
    _user_repo = Database.instance().user_repo
    
    def __init__(self, gateway_info: GatewayInfo):
        self.gateway_address = gateway_info.address
        self.session_port = gateway_info.port
        self._gateway_info = gateway_info
        self._message_handler = MessageHandler(gateway_info)
        self._error_handler = ErrorHandler(gateway_info)
        self._keep_alive_handler = KeepAliveHandler()
        self._waiting_timer = None
    
    def connect(self):
        self.start_session_phase()
    
    def send(self):
        DoActionRequest
        self._send_method()
    
    def start_session_phase(self):
        log_info(__name__, "Starting Session Phase...")
        config = self.get_config_for_session_phase()
        client = WSSessionPhase(config)
        client.connect()
        
    def start_attach_phase(self):
        log_info(__name__, "Starting Attach Phase...")
        config = self.get_config_for_attach_phase()
        client = WSAttachPhase(config)
        client.connect()    
    
    def get_config_for_session_phase(self) -> WebSocketConfig:
        config = self.get_config()
        config.on_close_callback = self.on_session_close_callback
        return config
    
    def get_config_for_attach_phase(self) -> WebSocketConfig:
        config = self.get_config()
        config.user_credentials = self._user_repo.get_current_user()
        config.on_open_callback = self.on_attach_connection_opened
        config.on_message_callback = self.on_attach_message_received
        config.on_error_message_callback = self.on_attach_error_message_received
        config.on_close_callback = self.on_attach_close_callback
        return config
    
    def on_session_close_callback(self, response: BaseResponse):
        log_info(__name__, "Session Phase Done!")
        self.attach_port = self.get_port_to_attach(response)
        self.start_attach_phase()

    def on_attach_connection_opened(self, send_method: Callable[[BaseRequestResponse], None]):
        self._send_method = send_method
        self._keep_alive_handler.set_handler(self.send_keep_alive)
    
    def on_attach_message_received(self, message: BaseRequestResponse) -> BaseRequestResponse:
        response = self._message_handler.message_received(message)
        self.handle_keep_alive(response)
        return response
        
    def on_attach_error_message_received(self, last_client_message: BaseRequestResponse, last_server_message: BaseRequestResponse, exception: Exception) -> BaseRequestResponse:
        try:
            response = self._error_handler.error_message_received(last_client_message, last_server_message, exception)
            self.handle_keep_alive(response)
            return response
        except ConnectionAbortedError:
            self.disconnect()
        
    def on_attach_close_callback(self, message: BaseRequestResponse):
        if isinstance(message, BaseRequest):
            self.attach_port = None
            self._keep_alive_handler.stop()
            seconds_to_wait = self.get_seconds_to_wait(message)
            log_info(__name__, f"Waiting {str(seconds_to_wait)} seconds before reconnecting...")
            time.sleep(seconds_to_wait)
            self.connect()
        
    def handle_keep_alive(self, message: BaseRequestResponse):
        if message:
            self._keep_alive_handler.reset()
    
    def send_keep_alive(self):
        keep_alive_request = BaseRequest(function = 'keepalive')
        response = self.on_attach_message_received(keep_alive_request)
        try:
            self._send_method(response)
        except WebSocketConnectionClosedException:
            self.disconnect()
    
    def get_config(self) -> WebSocketConfig:
        config = WebSocketConfig()
        config.gateway_info = self._gateway_info
        config.user_credentials = self._user_repo.get_current_user()
        config.address = self.gateway_address
        config.port = self.attach_port if self.attach_port else self.session_port
        return config
        
    def get_port_to_attach(self, response: BaseResponse) -> int:
        if response:
            return response.result[0]['communication']['ipport']
        self.disconnect()
    
    def get_seconds_to_wait(self, request: BaseRequest) -> int:
        if request and request.args:
            return int(request.args[0].get('value', 0))
        self.disconnect()
    
    def disconnect(self):
        log_info(__name__, "Terminating the execution...")
        self._keep_alive_handler.stop()
        exit()
