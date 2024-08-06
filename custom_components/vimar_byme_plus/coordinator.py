"""Provides the Vimar DataUpdateCoordinator."""

import asyncio
from datetime import timedelta
import logging

from requests.exceptions import ConnectTimeout, HTTPError
from xknx import XKNX

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN
from .vimar.vimar_client import VimarClient
from .vimar.model.vimar_data import VimarData

_LOGGER = logging.getLogger(__name__)


class VimarDataUpdateCoordinator(DataUpdateCoordinator[VimarData]):
    """Class to manage fetching VIMAR data."""

    client: VimarClient
    config: VimarData
    knx: XKNX

    def __init__(self, hass: HomeAssistant, data: dict[str, str]) -> None:
        """Initialize the coordinator."""
        self.client = VimarClient(data)
        self.knx = XKNX()
        interval = timedelta(seconds=DEFAULT_UPDATE_INTERVAL)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=interval)

    async def start(self):
        """Start coordinator processes."""
        # await self.knx.start()

    async def stop(self):
        """Stop coordinator processes."""
        await self.knx.stop()

    async def retrieve_data(self):
        """Validate Coordinator initialization."""
        ok = await self.client.login()
        if not ok:
            raise VimarLoginException
        return self.client.get_configuration_dict()

    async def _async_update_data(self) -> VimarData:
        """Fetch data from API endpoint."""
        _LOGGER.info("Updating coordinator")
        try:
            async with asyncio.timeout(15):
                return await self.hass.async_add_executor_job(self._update_data)
        except (ConnectTimeout, HTTPError) as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

    def _update_data(self) -> VimarData:
        _LOGGER.debug("Obtaining data")
        config_dict = self.client.get_configuration_dict()
        self.config = VimarData(config_dict)
        return self.config


class VimarLoginException(BaseException):
    """Exception class to handle login error."""
