"""Provides the Vimar DataUpdateCoordinator."""

from ..config.const import USERNAME
from ..database.database import Database
from ..mapper.vimar_data.vimar_data_mapper import VimarDataMapper
from ..model.exception.code_not_valid_exception import CodeNotValidException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.gateway.vimar_data import VimarData
from ..service.integration_service import IntegrationService
from ..utils.logger import log_info
from ..utils.thread import Thread
from ..utils.thread_monitor import thread_exists


class VimarClient:
    """Class to manage fetching VIMAR data."""

    _integration_service: IntegrationService
    _component_repo = Database.instance().component_repo
    _user_repo = Database.instance().user_repo
    _thread_name = "VimarServiceThread"

    def __init__(self, gateway_info: GatewayInfo) -> None:
        """Initialize the coordinator."""
        self._integration_service = IntegrationService(gateway_info)

    def start(self):
        if not self.has_gateway_info():
            log_info(__name__, "GatewayInfo not found, skipping connection...")
            return
        if not self.has_credentials():
            log_info(__name__, "Credentials not found, skipping connection...")
            return
        if not self.already_connected():
            log_info(__name__, "Already connected with Gateway, skipping connection...")
        log_info(__name__, "Connecting to Gateway, please wait...")
        self.connect()

    async def stop(self):
        """Stop coordinator processes."""
        #

    def connect(self):
        """Start Vimar connection process."""
        thread = Thread(
            target=self._integration_service.connect,
            name=self._thread_name,
            daemon=True,
        )
        thread.start()

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
        return thread_exists(self._thread_name)

    def set_setup_code(self, setup_code: str):
        self.validate_code(setup_code)
        self._user_repo.insert_setup_code(USERNAME, setup_code)

    def validate_code(self, code: str):
        """Validate the setup code syntax."""
        if not code.isdigit() or len(code) != 4:
            raise CodeNotValidException
