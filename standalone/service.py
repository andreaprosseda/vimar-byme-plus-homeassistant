from .vimar.service.gateway_founder_service import GatewayFounderService
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.client.vimar_client import VimarClient
from .vimar.model.exception.code_not_valid_exception import CodeNotValidException
from .vimar.model.gateway.vimar_data import VimarData

class StandAloneService:
    
    _client: VimarClient
    
    def __init__(self):
        gateway_info = self.get_gateway_info()
        self._client = VimarClient(gateway_info)
    
    def get_gateway_info(self) -> GatewayInfo:
        founder = GatewayFounderService()
        gateway_info = founder.search()
        return gateway_info
    
    def start(self):
        self._client.start()
    
    def retrieve_data(self) -> VimarData:
        return self._client.retrieve_data()

    def request_status_code_if_needed(self):
        if self._client.has_credentials():
            return
        
        while True:
            try:
                status_code = input("Enter Status Code [4-digit]: ")
                return self._client.set_setup_code(status_code)
            except CodeNotValidException:
                print("Status Code not valid, please try again")
