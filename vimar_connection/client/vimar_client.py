from typing import Optional
from .credential_manager import CredentialManager
from .integration_manager import IntegrationManager
from .web_socket.ws_session_phase import WSSessionPhase
from .web_socket.ws_attach_phase import WSAttachPhase
from ..model.gateway_info import GatewayInfo
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..model.web_socket.base_request import BaseRequest

class VimarClient:
    
    _gateway_info: GatewayInfo
    _integration_manager: IntegrationManager
    _credential_manager: CredentialManager
    
    attach_port: Optional[int] = None
    
    def __init__(self, gateway_info: GatewayInfo):
        self._gateway_info = gateway_info
        self._credential_manager = CredentialManager()
        self._integration_manager = IntegrationManager(gateway_info)

    def connect(self):
        self.start_session_phase()
    
    def start_session_phase(self):
        config = self.get_config_for_session_phase()
        client = WSSessionPhase(config)
        client.connect()
        
    def on_session_close_callback(self, response: dict):
        self.attach_port = self.get_port_to_attach(response)
        self.start_attach_phase()
    
    def start_attach_phase(self):
        config = self.get_config_for_attach_phase()
        client = WSAttachPhase(config)
        client.connect()
        
    def on_attach_message_callback(self, response: dict) -> BaseRequest:
        return self._integration_manager.message_received(response)
    
    def on_attach_error_message_callback(self, response: dict) -> BaseRequest:
        return self._integration_manager.error_message_received(response)
        
    def get_port_to_attach(self, response: dict) -> int:
        return response['result'][0]['communication']['ipport']
    
    def get_config(self) -> WebSocketConfig:
        config = WebSocketConfig()
        config.gateway_info = self._gateway_info
        config.user_credentials = self._credential_manager.get_user_credentials()
        config.address = self._gateway_info.address
        config.port = self.attach_port if self.attach_port else self._gateway_info.port
        return config
    
    def get_config_for_session_phase(self) -> WebSocketConfig:
        config = self.get_config()
        config.on_close_callback = self.on_session_close_callback
        return config
    
    def get_config_for_attach_phase(self) -> WebSocketConfig:
        config = self.get_config()
        config.user_credentials = self._credential_manager.get_user_credentials()
        config.on_message_callback = self.on_attach_message_callback
        config.on_error_message_callback = self.on_attach_error_message_callback
        return config
    
    def get_config_for_ambient_discovery_phase(self) -> WebSocketConfig:
        config = self.get_config()
        return config