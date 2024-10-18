"""Provides the Vimar DataUpdateCoordinator."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CODE, DEFAULT_UPDATE_INTERVAL, DOMAIN
from .vimar.client.vimar_client import VimarClient
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.gateway.vimar_data import VimarData

_LOGGER = logging.getLogger(__name__)


class VimarDataUpdateCoordinator(DataUpdateCoordinator[VimarData]):
    """Vimar coordinator."""

    gateway_info: GatewayInfo
    client: VimarClient

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        self.gateway_info = GatewayInfo()
        self.client = VimarClient(self.gateway_info)

        interval = timedelta(seconds=DEFAULT_UPDATE_INTERVAL)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=interval)

    async def initialize(self, user_input: dict[str, str]):
        """Initialize coordinator processes."""
        code = user_input[CODE]
        self.client.set_setup_code(code)

    async def start(self):
        """Start coordinator processes."""
        self.client.start()

    async def stop(self):
        """Stop coordinator processes."""
        # await self.knx.stop()

    async def _async_update_data(self) -> VimarData:
        """Get the latest data."""
        return self.client.retrieve_data()
        # return await self.hass.async_add_executor_job(self._sync_update)
