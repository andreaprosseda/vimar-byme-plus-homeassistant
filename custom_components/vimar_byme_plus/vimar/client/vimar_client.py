"""Provides the Vimar DataUpdateCoordinator."""

from ..config.const import USERNAME
from ..database.database import Database
from ..mapper.vimar_data.vimar_data_mapper import VimarDataMapper
from ..model.exceptions import CodeNotValidException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.gateway.vimar_data import VimarData
from ..model.repository.user_credentials import UserCredentials
from ..service.integration_service import IntegrationService
from ..utils.logger import log_info


class VimarClient:
    """Class to manage fetching VIMAR data."""

    _integration_service: IntegrationService
    _component_repo = Database.instance().component_repo
    _user_repo = Database.instance().user_repo

    def __init__(self, gateway_info: GatewayInfo) -> None:
        """Initialize the coordinator."""
        self._integration_service = IntegrationService(gateway_info)

    def test_connection(self):
        """Test the Vimar WebSocket connection."""
        if self._can_connect():
            self._integration_service.test_connection()

    def connect(self):
        """Handle the Vimar WebSocket connection."""
        if self._can_connect():
            self._integration_service.connect()

    def _can_connect(self) -> bool:
        if not self.has_gateway_info():
            log_info(__name__, "GatewayInfo not found, skipping connection...")
            return False
        if not self.has_credentials():
            log_info(__name__, "Credentials not found, skipping connection...")
            return False
        # if not self.already_connected():
        #     log_info(__name__, "Already connected with Gateway, skipping connection...")
        #     return False
        log_info(__name__, "Connecting to Gateway, please wait...")
        return True

    async def stop(self):
        """Stop coordinator processes."""
        # self._integration_service

    def retrieve_data(self) -> VimarData:
        """Get the latest data from DB."""
        components = self._component_repo.get_all()
        return VimarDataMapper.from_list(components)

    def get_gateway_info(self) -> GatewayInfo:
        return self._integration_service.gateway_info

    def has_gateway_info(self) -> bool:
        return self._integration_service.gateway_info is not None

    def has_credentials(self) -> bool:
        credentials = self._user_repo.get_current_user()
        return credentials is not None

    def already_connected(self) -> bool:
        return self._integration_service.web_socket is not None

    def set_setup_code(self, setup_code: str):
        self.validate_code(setup_code)
        current_user = self._user_repo.get_current_user()
        if not self.same_code(setup_code, current_user):
            self._user_repo.insert_setup_code(USERNAME, setup_code)

    def same_code(self, setup_code: str, current_user: UserCredentials) -> bool:
        if not current_user:
            return False
        return current_user.setup_code == setup_code

    def validate_code(self, code: str):
        """Validate the setup code syntax."""
        if not code.isdigit() or len(code) != 4:
            raise CodeNotValidException
