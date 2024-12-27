"""Provides the Vimar DataUpdateCoordinator."""

from ..config.const import USERNAME
from ..database.database import Database
from ..mapper.vimar_data_mapper import VimarDataMapper
from ..model.component.vimar_component import VimarComponent
from ..model.enum.action_type import ActionType
from ..model.exceptions import CodeNotValidException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.gateway.vimar_data import VimarData
from ..model.repository.user_credentials import UserCredentials
from ..service.association_service import AssociationService
from ..service.operational_service import OperationalService, Update
from ..utils.logger import log_info
from ..utils.thread import Thread


class VimarClient:
    """Class to manage fetching VIMAR data."""

    _association_service: AssociationService
    _operational_service: OperationalService
    _component_repo = Database.instance().component_repo
    _user_repo = Database.instance().user_repo
    _thread_name = "VimarServiceThread"

    def __init__(self, gateway_info: GatewayInfo, callback: Update) -> None:
        """Initialize the coordinator."""
        self._association_service = AssociationService(gateway_info)
        self._operational_service = OperationalService(gateway_info, callback)

    def association_phase(self):
        """Start the association phase for Vimar connection."""
        self._association_service.associate()
        self._association_service.complete()

    def operational_phase(self):
        """Start the operational phase for Vimar connection."""
        if self._can_connect():
            self.connect()

    def connect(self):
        """Create a new thread for Operational Phase interaction."""
        thread = Thread(
            target=self._operational_service.connect,
            name=self._thread_name,
            daemon=True,
        )
        thread.start()

    def send(self, component: VimarComponent, action_type: ActionType, *args):
        """Send a request coming from HomeAssistant to Gateway."""
        self._operational_service.send_action(component, action_type, *args)

    def get_status(self, idsf: int):
        """Send a request coming from HomeAssistant to Gateway."""
        self._operational_service.send_get_status(idsf)

    def stop(self):
        """Stop coordinator processes."""
        self._operational_service.disconnect()

    def retrieve_data(self) -> VimarData:
        """Get the latest data from DB."""
        components = self._component_repo.get_all()
        return VimarDataMapper.from_list(components)

    def get_gateway_info(self) -> GatewayInfo:
        return self._operational_service.gateway_info

    def has_gateway_info(self) -> bool:
        return self._operational_service.gateway_info is not None

    def has_credentials(self) -> bool:
        credentials = self._user_repo.get_current_user()
        return credentials and credentials.password is not None

    def set_setup_code(self, setup_code: str):
        if not setup_code:
            return
        self.validate_code(setup_code)
        self._user_repo.insert_setup_code(USERNAME, setup_code)

    def same_code(self, setup_code: str, current_user: UserCredentials) -> bool:
        if not current_user:
            return False
        return current_user.setup_code == setup_code

    def validate_code(self, code: str):
        """Validate the setup code syntax."""
        if not code or not code.isdigit() or len(code) != 4:
            raise CodeNotValidException

    def _can_connect(self) -> bool:
        if not self.has_gateway_info():
            log_info(__name__, "GatewayInfo not found, skipping connection...")
            return False
        if not self.has_credentials():
            log_info(__name__, "Credentials not found, skipping connection...")
            return False
        log_info(__name__, "Connecting to Gateway, please wait...")
        return True
