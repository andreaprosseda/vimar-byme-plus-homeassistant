"""Provides the Vimar Coordinator."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import GATEWAY_NAME, ADDRESS, PORT, GATEWAY_ID, HOST, PROTOCOL, CODE, DEFAULT_UPDATE_INTERVAL, DOMAIN
from .vimar.client.vimar_client import VimarClient
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.gateway.vimar_data import VimarData
from .vimar.utils.logger import log_debug

_LOGGER = logging.getLogger(__name__)


class Coordinator(DataUpdateCoordinator[VimarData]):
    """Vimar coordinator."""

    gateway_info: GatewayInfo
    client: VimarClient

    def __init__(self, hass: HomeAssistant, user_input: dict[str, str]) -> None:
        """Initialize the coordinator."""
        self.gateway_info = self._get_gateway_info(user_input)
        self.client = VimarClient(self.gateway_info)
        self.client.set_setup_code(user_input[CODE])

        interval = timedelta(seconds=DEFAULT_UPDATE_INTERVAL)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=interval)

    def associate(self):
        """Test coordinator processes."""
        self.client.association_phase()

    def start(self):
        """Start coordinator processes."""
        self.client.operational_phase()

    async def stop(self):
        """Stop coordinator processes."""
        self.client.stop()

    async def _async_update_data(self) -> VimarData:
        """Get the latest data."""
        return self.client.retrieve_data()
        # return await self.hass.async_add_executor_job(self._sync_update)

    def _get_gateway_info(self, user_input: dict[str, str]) -> GatewayInfo:
        return GatewayInfo(
            host=user_input[HOST],
            address=user_input[ADDRESS],
            port=user_input[PORT],
            deviceuid=user_input[GATEWAY_ID],
            plantname=user_input[GATEWAY_NAME],
            protocolversion=user_input[PROTOCOL]
        )
        