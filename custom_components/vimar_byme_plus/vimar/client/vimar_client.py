"""Provides the Vimar DataUpdateCoordinator."""

from ..config.const import USERNAME
from ..database.database import Database
from ..mapper.vimar_data_mapper import VimarDataMapper
from ..model.component.vimar_component import VimarComponent
from ..model.enum.action_type import ActionType
from ..model.exceptions import CodeNotValidException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.gateway.vimar_data import VimarData
from ..model.integration_options import IntegrationOptions
from ..model.repository.user_credentials import UserCredentials
from ..service.association_service import AssociationService
from ..service.operational_service import OperationalService, Update
from ..database.repository.component_repo import ComponentRepo
from ..database.repository.user_repo import UserRepo

from ..utils.logger import log_info
from ..utils.thread import Thread
from ..utils.thread_monitor import thread_exists


class VimarClient:
    """Class to manage fetching VIMAR data."""

    _association_service: AssociationService
    _operational_service: OperationalService
    _component_repo: ComponentRepo
    _user_repo: UserRepo
    _thread_name = "VimarServiceThread"

    def __init__(self, gateway_info: GatewayInfo, callback: Update) -> None:
        """Initialize the coordinator."""
        db = Database.instance(gateway_info.deviceuid)
        self._component_repo = db.component_repo
        self._user_repo = db.user_repo
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

    def reconnect(self):
        """Force a tear-down and a fresh connect.

        Used by the HA watchdog when the daemon thread has died or the
        gateway has gone silent. Disconnect best-effort, then re-enter
        operational_phase to spawn a new VimarServiceThread.
        """
        try:
            self._operational_service.disconnect()
        except Exception:  # pylint: disable=broad-except
            log_info(__name__, "Disconnect raised; ignoring and re-attaching.")
        self.operational_phase()

    def is_thread_alive(self) -> bool:
        """Return True if the Vimar service daemon thread is running."""
        return thread_exists(self._thread_name)

    @property
    def seconds_since_last_message(self) -> float:
        """Seconds since the gateway last sent any message."""
        return self._operational_service.seconds_since_last_message

    def send(self, component: VimarComponent, action_type: ActionType, *args):
        """Send a request coming from HomeAssistant to Gateway."""
        self._operational_service.send_action(component, action_type, *args)

    def get_status(self, idsf: int):
        """Send a request coming from HomeAssistant to Gateway."""
        self._operational_service.send_get_status(idsf)

    def stop(self):
        """Stop coordinator processes."""
        self._operational_service.disconnect()

    def retrieve_data(self, options: IntegrationOptions | None = None) -> VimarData:
        """Get the latest data from DB."""
        components = self._component_repo.get_all()
        return VimarDataMapper.from_list(components, options or IntegrationOptions())

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
