from .vimar.service.gateway_founder_service import GatewayFounderService
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.client.vimar_client import VimarClient
from .vimar.model.exceptions import CodeNotValidException
from .vimar.model.gateway.vimar_data import VimarData


class StandAloneService:
    _client: VimarClient

    def __init__(self):
        gateway_info = self.get_gateway_info()
        self._client = VimarClient(gateway_info, None)

    def get_gateway_info(self) -> GatewayInfo:
        founder = GatewayFounderService()
        gateway_info = founder.search()
        return gateway_info

    def association_phase(self):
        self._client.association_phase()

    def operational_phase(self):
        self._client.operational_phase()

    def send_get_status(self, idsf: int):
        self._client.get_status(idsf)

    def retrieve_data(self) -> VimarData:
        return self._client.retrieve_data()

    def request_setup_code_if_needed(self) -> bool:
        if self._client.has_credentials():
            return False

        while True:
            try:
                status_code = input("Enter Setup Code [4-digit]: ")
                self._client.set_setup_code(status_code)
                return True
            except CodeNotValidException:
                print("Setup Code not valid, please try again")
