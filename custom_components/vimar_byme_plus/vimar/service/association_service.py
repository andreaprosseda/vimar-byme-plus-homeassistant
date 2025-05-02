from ..client.authenticator_client import AuthenticatorClient
from ..client.web_service.sync_attach_phase import SyncAttachPhase
from ..client.web_service.sync_session_phase import SyncSessionPhase
from ..database.database import Database
from ..model.exceptions import VimarErrorResponseException
from ..model.gateway.gateway_info import GatewayInfo
from ..model.repository.user_credentials import UserCredentials
from ..model.web_socket.base_response import BaseResponse
from ..model.web_socket.web_socket_config import WebSocketConfig
from ..utils.logger import log_info
from .handler.message_handler.message_handler import MessageHandler


class AssociationService:
    gateway_address: str
    session_port: int
    gateway_info: GatewayInfo

    attach_port: int | None = None

    _message_handler: MessageHandler
    _user_repo = Database.instance().user_repo
    _authenticator_client = AuthenticatorClient()

    def __init__(self, gateway_info: GatewayInfo) -> None:
        """Initialize Vimar intagration."""
        self.gateway_address = gateway_info.address
        self.session_port = gateway_info.port
        self.gateway_info = gateway_info
        self._message_handler = MessageHandler(gateway_info)

    def associate(self):
        """Handle the connection Vimar WebSocket connection."""
        try:
            self.clean()
            log_info(__name__, "Starting Association | Session Phase...")
            self.sync_session_phase()
            log_info(__name__, "Association | Session Phase Done!")
            log_info(__name__, "Starting Association | Attach Phase...")
            attach_response = self.sync_attach_phase()
            self.save_attach_credentials(attach_response)
            log_info(__name__, "Association | Attach Phase Done!")
        except Exception as err:
            raise VimarErrorResponseException(err) from err

    def complete(self):
        """Handle the connection Vimar WebSocket connection."""
        try:
            self.clean()
            log_info(__name__, "Starting Operational | Session Phase...")
            self.sync_session_phase()
            log_info(__name__, "Operational | Session Phase Done!")
            log_info(__name__, "Starting Operational | Attach Phase...")
            self.sync_attach_phase()
            log_info(__name__, "Operational | Attach Phase Done!")
        except Exception as err:
            raise VimarErrorResponseException(err) from err

    def clean(self):
        self.attach_port = None
        self._message_handler.clean()

    def sync_session_phase(self):
        """Handle SessionPhase interaction."""
        port = self.session_port
        handler = self._message_handler
        config = self._get_config(port)
        client = SyncSessionPhase(config, handler)
        self.attach_port = client.connect()

    def sync_attach_phase(self) -> BaseResponse:
        """Handle AttachPhase interaction."""
        port = self.attach_port
        handler = self._message_handler
        credentials = self.get_signed_credentials()
        config = self._get_config(port, credentials)
        client = SyncAttachPhase(config, handler)
        return client.connect()

    def _get_config(
        self, port: int, user_credentials: UserCredentials = None
    ) -> WebSocketConfig:
        config = WebSocketConfig()
        config.gateway_info = self.gateway_info
        config.user_credentials = user_credentials
        config.address = self.gateway_address
        config.port = port
        return config

    def get_signed_credentials(self) -> UserCredentials:
        client = self._authenticator_client
        credentials = self._user_repo.get_current_user()
        if credentials and credentials.password:
            return credentials
        signed_credentials = client.get_association_credentials(credentials)
        self._user_repo.update(signed_credentials)
        return signed_credentials

    def save_attach_credentials(self, response: BaseResponse):
        client = self._authenticator_client
        credentials = UserCredentials.obj_from_dict(response)
        signed_credentials = client.get_operational_credentials(credentials)
        signed_credentials.plant_name = credentials.plant_name
        self._user_repo.update(signed_credentials)
