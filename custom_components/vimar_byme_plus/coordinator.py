"""Provides the Vimar DataUpdateCoordinator."""

from dataclasses import asdict
from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CODE, DEFAULT_UPDATE_INTERVAL, DOMAIN
from .vimar.config.const import USERNAME
from .vimar.database.database import Database
from .vimar.model.enum.component_type import ComponentType
from .vimar.model.exception.setup_code_not_valid_exception import (
    SetupCodeNotValidException,
)
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.repository.user_component import UserComponent
from .vimar.service.integration_service import IntegrationService
from .vimar.utils.logger import log_info, log_debug
from .vimar.utils.thread import Thread

_LOGGER = logging.getLogger(__name__)


class VimarDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching VIMAR data."""

    _integration_service: IntegrationService
    _component_repo = Database.instance().component_repo
    _user_repo = Database.instance().user_repo

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        gateway_info = GatewayInfo()
        self._integration_service = IntegrationService(gateway_info)

        interval = timedelta(seconds=DEFAULT_UPDATE_INTERVAL)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=interval)

    async def initialize(self, user_input: dict[str, str]):
        code = user_input[CODE]
        self.set_setup_code(code)

    async def start(self):
        if not self.has_gateway_info():
            log_info(__name__, "GatewayInfo not found, skipping connection...")
            return
        if not self.has_credentials():
            log_info(__name__, "Credentials not found, skipping connection...")
            return
        log_info(__name__, "Connecting to Gateway, please wait...")
        await self.connect()

    async def stop(self):
        """Stop coordinator processes."""
        # await self.knx.stop()

    async def connect(self):
        """Start Vimar connection process."""
        thread = Thread(
            target=self._integration_service.connect,
            name="VimarServiceThread",
            daemon=True,
        )
        thread.start()

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Get the latest data."""
        return await self.hass.async_add_executor_job(self._sync_update)

    def _sync_update(self) -> dict[str, dict[str, Any]]:
        """Get the latest data from the Qnap API."""
        return {
            "status": "verify if it could be done with callback, instead of polling"
        }

    def get_components(self, type: ComponentType) -> list[UserComponent]:
        """Get components list from database, filtered by type."""
        components = self._component_repo.get_component_of_type(type.id())
        log_debug(__name__, f"Elements '{type.device_class()}' found: {len(components)}")

    def get_gateway_info(self) -> GatewayInfo:
        return self._integration_service.gateway_info

    def has_gateway_info(self) -> bool:
        return self._integration_service.gateway_info is not None

    def has_credentials(self) -> bool:
        credentials = self._user_repo.get_current_user()
        return credentials is not None

    def set_setup_code(self, setup_code: str):
        self.validate_code(setup_code)
        self._user_repo.insert_setup_code(USERNAME, setup_code)

    def validate_code(self, code: str):
        """Validate the setup code syntax."""
        if not code.isdigit() or len(code) != 4:
            raise SetupCodeNotValidException
