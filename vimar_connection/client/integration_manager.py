from .credential_manager import CredentialManager
from .home_manager import HomeManager
from ..model.gateway_info import GatewayInfo
from ..model.web_socket.base_request import BaseRequest
from ..model.enum.integration_phase import IntegrationPhase
from ..model.web_socket.attach_request import AttachRequest
from ..model.web_socket.detach_request import DetachRequest
from ..model.web_socket.ambient_discovery_request import AmbientDiscoveryRequest
from ..model.web_socket.sf_discovery_request import SfDiscoveryRequest
from ..utils.session_token import get_session_token

class IntegrationManager:
    
    _gateway_info: GatewayInfo
    _credential_manager: CredentialManager
    _home_manager: HomeManager
    _token = None
    
    def __init__(self, gateway_info: GatewayInfo):
        self._gateway_info = gateway_info
        self._credential_manager = CredentialManager()
        self._home_manager = HomeManager()
        self._token = get_session_token()
    
    def message_received(self, response: dict) -> BaseRequest:
        response_phase = self.get_phase(response)
        match response_phase:
            case IntegrationPhase.SESSION:
                return self.handle_session_response(response)
            case IntegrationPhase.ATTACH:
                return self.handle_attach_response(response)
            case IntegrationPhase.AMBIENT_DISCOVERY:
                return self.handle_ambient_discovery_response(response)
            case IntegrationPhase.SF_DISCOVERY:
                return self.handle_sf_discovery_response(response)
            case IntegrationPhase.REGISTER:
                return self.handle_register_response(response)
            case IntegrationPhase.DETACH:
                return self.handle_detach_response(response)
            case _:
                print("Unknown Phase")
                return self.get_detach_request()
        
    def error_message_received(self, response: dict) -> BaseRequest:
        if response:
            return self.get_detach_request()
        return None
        
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
        self._home_manager.save_environments(response)
        return self.get_sf_discovery_request()
    
    def handle_sf_discovery_response(self, response: dict) -> BaseRequest:
        print('SF Discovery Phase completed, sending Register Request...')
        return self.get_detach_request()#get_register_request()
    
    def handle_register_response(self, response: dict) -> BaseRequest:
        print('Register Phase completed, ...')
        return self.todo()
    
    def handle_detach_response(self, response: dict) -> BaseRequest:
        print('Detach Phase completed')
        return None
    
    def get_attach_request(self) -> AttachRequest:
        return AttachRequest(
            target=self._gateway_info.deviceuid,
            token=self._token,
            protocol_version=self._gateway_info.protocolversion,
            user_credentials=self._credential_manager.get_user_credentials()
        )
        
    def get_detach_request(self) -> DetachRequest:
        return DetachRequest(
            target=self._gateway_info.deviceuid,
            token=self._token
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
            ambient_ids=self._home_manager.get_ambient_ids()
        )
    
    def get_register_request(self) -> BaseRequest:
        pass
    
    def todo(self) -> BaseRequest:
        pass