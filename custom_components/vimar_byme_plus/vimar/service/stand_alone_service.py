from .gateway_founder_service import GatewayFounderService
from .integration_service import IntegrationService
from ..model.repository.user_credentials import UserCredentials
from ..model.gateway.gateway_info import GatewayInfo
from ..database.database import Database
from ..config.const import USERNAME
from ..utils.logger import log_info, log_debug
from ..utils.thread import Thread

class StandAloneService:
    _user_repo = Database.instance().user_repo
    _integration_service: IntegrationService = None
    _gateway_info: GatewayInfo = None

    def __init__(self):
        self._gateway_info = self.get_gateway_info()
        self._integration_service = IntegrationService(self._gateway_info)

    def request_status_code_if_needed(self):
        if self._has_credentials():
            return
        
        while True:
            status_code = input("Enter Status Code [4-digit]: ")
            if status_code.isdigit() and len(status_code) == 4:
                return self._set_credentials(status_code)
            else:
                print("Status Code not valid, please try again")

    def start(self):    
        vimar_thread = Thread(target=self._start, name="VimarThread", daemon=True)
        vimar_thread.start()

    def _start(self):
        self._integration_service.connect()

    def get_gateway_info(self) -> GatewayInfo:
        founder = GatewayFounderService()
        gateway_info = founder.search()
        return gateway_info

    def has_gateway_info(self) -> bool:
        return self._gateway_info is not None

    def _has_credentials(self) -> bool:
        log_debug(__name__, "Retrieving credentials from database...")
        credentials = self._user_repo.get_current_user()
        found = credentials is not None
        log_info(__name__, f"Credentials found: {found}")
        return found

    def _set_credentials(self, setup_code: str):
        credentials = UserCredentials(username=USERNAME, setup_code=setup_code)
        self._user_repo.delete_all()
        self._user_repo.insert(credentials)
