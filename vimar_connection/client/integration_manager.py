import asyncio
from typing import Callable
from .credential_manager import CredentialManager
from .home_manager import HomeManager
from .keep_alive_handler import KeepAliveHandler
from ..model.gateway_info import GatewayInfo
from ..model.web_socket.base_request import BaseRequest
from ..model.enum.integration_phase import IntegrationPhase
from ..model.web_socket.request.attach_request import AttachRequest
from ..model.web_socket.request.detach_request import DetachRequest
from ..model.web_socket.request.ambient_discovery_request import AmbientDiscoveryRequest
from ..model.web_socket.request.sf_discovery_request import SfDiscoveryRequest
from ..model.web_socket.request.register_request import RegisterRequest
from ..model.web_socket.request.keep_alive_request import KeepAliveRequest
from ..model.web_socket.response.changestatus_response import ChangeStatusResponse
from ..model.web_socket.response.expire_response import ExpireResponse
from ..utils.session_token import get_session_token

class IntegrationManager:
    
    _gateway_info: GatewayInfo
    _credential_manager: CredentialManager
    _keep_alive_handler: KeepAliveHandler
    _home_manager: HomeManager
    
    _send_method: Callable[[BaseRequest], None]
    _token = None
    _last_msgid = 0
    
    def __init__(self, gateway_info: GatewayInfo):
        self._gateway_info = gateway_info
        self._credential_manager = CredentialManager()
        self._keep_alive_handler = KeepAliveHandler()
        self._home_manager = HomeManager()
        self._token = get_session_token()
    
    def connection_opened(self, send_method: Callable[[BaseRequest], None]):
        self._send_method = send_method
        self._keep_alive_handler.set_handler(self.send_keep_alive)
    
    def message_received(self, message: dict) -> BaseRequest:
        self._last_msgid = int(message.get('msgid', -1))
        phase = self.get_phase(message)
        match phase:
            case IntegrationPhase.SESSION:
                return self.handle_session_response(message)
            case IntegrationPhase.ATTACH:
                return self.handle_attach_response(message)
            case IntegrationPhase.AMBIENT_DISCOVERY:
                return self.handle_ambient_discovery_response(message)
            case IntegrationPhase.SF_DISCOVERY:
                return self.handle_sf_discovery_response(message)
            case IntegrationPhase.CHANGE_STATUS:
                return self.handle_change_status_request(message)
            case IntegrationPhase.EXPIRE:
                return self.handle_expire_request(message)
            case IntegrationPhase.REGISTER:
                return self.idle()
            case IntegrationPhase.KEEP_ALIVE:
                return self.idle()
            case IntegrationPhase.DETACH:
                return self.idle()
            case _:
                print("Unknown Phase!!!")
                return self.get_detach_request()
        
    def error_message_received(self, response: dict) -> BaseRequest:
        if response:
            return self.get_detach_request()
        return None
    
    def send_keep_alive(self):
        request = self.get_keep_alive_request()
        self._send_method(request)
        
    def get_phase(self, response: dict) -> IntegrationPhase:
        function = response['function']
        return IntegrationPhase.get(function)
    
    def handle_session_response(self, response: dict) -> AttachRequest:
        print('Session phase completed, sending Attach Request...')
        return self.get_attach_request()
    
    def handle_attach_response(self, response: dict) -> AmbientDiscoveryRequest:
        print('Attach Phase completed, sending Ambient Discovery Request...')
        self._credential_manager.save_user_credentials(response)
        self._token = response['result'][0]['token']
        return self.get_ambient_discovery_request()
    
    def handle_ambient_discovery_response(self, response: dict) -> SfDiscoveryRequest:
        print('Ambient Discovery Phase completed, sending SF Discovery Request...')
        self._home_manager.save_ambients(response)
        return self.get_sf_discovery_request()
    
    def handle_sf_discovery_response(self, response: dict) -> RegisterRequest:
        print('SF Discovery Phase completed, sending Register Request...')
        self._home_manager.save_components(response)
        return self.get_register_request()
    
    def handle_change_status_request(self, request: dict) -> ChangeStatusResponse:
        print('Change Status received, saving content...')
        self._home_manager.save_component_changes(request)
        return self.get_change_status_response(request)
        
    def handle_expire_request(self, request: dict) -> BaseRequest:
        print('Expire Request received, trying to reconnect...')
        self._keep_alive_handler.stop()        
        return self.idle()
        # if (value in seconds try to execute new sssion)
        # wait and then reconnect
        
    def get_attach_request(self) -> AttachRequest:
        return AttachRequest(
            target=self._gateway_info.deviceuid,
            token=self._token,
            protocol_version=self._gateway_info.protocolversion,
            user_credentials=self._credential_manager.get_user_credentials()
        )
        
    def get_ambient_discovery_request(self) -> AmbientDiscoveryRequest:
        return AmbientDiscoveryRequest(
            target=self._gateway_info.deviceuid,
            token=self._token
        )
    
    def get_sf_discovery_request(self) -> SfDiscoveryRequest:
        return SfDiscoveryRequest(
            target=self._gateway_info.deviceuid,
            token=self._token,
            ambient_ids=self._home_manager.get_all_ambient_ids()
        )
    
    def get_register_request(self) -> RegisterRequest:
        return RegisterRequest(
            target=self._gateway_info.deviceuid,
            token=self._token,
            components=self._home_manager.get_all_components()
        )
        
    def get_change_status_response(self, request: dict) -> ChangeStatusResponse:
        required_response = request['params'][0]['requiredresp']
        if not required_response:
            return None
        
        return ChangeStatusResponse(
            target=self._gateway_info.deviceuid,
            token=self._token,
            msgid=self._last_msgid + 1
        )
        
    # def get_expire_response(self, request: dict) -> ExpireResponse:
    #     required_response = request['params'][0]['requiredresp']
    #     if not required_response:
    #         return None
        
    #     return ExpireResponse(
    #         target=self._gateway_info.deviceuid,
    #         token=self._token,
    #         msgid=self._last_msgid + 1
    #     )
        
    def get_detach_request(self) -> DetachRequest:
        return DetachRequest(
            target=self._gateway_info.deviceuid,
            token=self._token,
            msgid=self._last_msgid + 1
        )
        
    def get_keep_alive_request(self) -> KeepAliveRequest:
        return KeepAliveRequest(
            target=self._gateway_info.deviceuid,
            token=self._token,
            msgid=self._last_msgid + 1
        )
    
    def idle(self):
        print("Entering idle state: no action required for this phase...")
        return None
    