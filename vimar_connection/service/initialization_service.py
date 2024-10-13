from .gateway_founder_service import GatewayFounderService
from .integration_service import IntegrationService
from ..model.repository.user_credentials import UserCredentials
from ..model.gateway.gateway_info import GatewayInfo
from ..database.database import Database
from ..config.const import USERNAME
from ..utils.logger import log_info, log_debug

class InitializationService:
    
    _user_repo = Database.instance().user_repo
        
    def start(self):
        self.check_credentials()
        gateway_info = self.get_gateway_info()
        integration_service = IntegrationService(gateway_info)
        integration_service.connect()
    
    def get_gateway_info(self) -> GatewayInfo:
        founder = GatewayFounderService()
        gateway_info = founder.search()
        return gateway_info
    
    def check_credentials(self) -> UserCredentials:
        credentials = self._user_repo.get_current_user()
        log_debug(__name__, f"Retrieving credentials: {credentials}")
        if credentials:
            log_info(__name__, f"Credentials found for username: {credentials.username}")
        else:
            code = input('Enter setup code obtained from Vimar PRO:\n')
            credentials = UserCredentials(username = USERNAME, setup_code = code)
            self._user_repo.delete_all()
            self._user_repo.insert(credentials)
