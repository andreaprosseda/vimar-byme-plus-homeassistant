"""Provides the Vimar Coordinator."""

import logging

from websocket import WebSocketConnectionClosedException

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    ADDRESS,
    CODE,
    DOMAIN,
    GATEWAY_ID,
    GATEWAY_NAME,
    HOST,
    PORT,
    PROTOCOL,
    SECTION_COUNTERS,
)
from .vimar.client.vimar_client import VimarClient
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.action_type import ActionType
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.gateway.vimar_data import VimarData
from .vimar.model.integration_options import IntegrationOptions

_LOGGER = logging.getLogger(__name__)


class Coordinator(DataUpdateCoordinator[VimarData]):
    """Vimar coordinator."""

    gateway_info: GatewayInfo
    client: VimarClient

    def __init__(
        self, hass: HomeAssistant, user_input: dict[str, str], entry: ConfigEntry | None = None
    ) -> None:
        """Initialize the coordinator."""
        self._entry = entry
        self.gateway_info = self._get_gateway_info(user_input)
        self.client = VimarClient(self.gateway_info, self.update_data)
        self.client.set_setup_code(user_input.get(CODE))

        super().__init__(hass, _LOGGER, name=DOMAIN)

    @property
    def options(self) -> IntegrationOptions:
        """Materialise entry.options into the runtime options bundle."""
        if self._entry is None:
            return IntegrationOptions()
        raw = self._entry.options or {}
        return IntegrationOptions(
            counter_types=raw.get(SECTION_COUNTERS, {}) or {},
        )

    def associate(self):
        """Test coordinator processes."""
        self.client.association_phase()

    def start(self):
        """Start coordinator processes."""
        self.client.operational_phase()
        self.update_data()

    def stop(self):
        """Stop coordinator processes."""
        self.client.stop()

    def send(self, component: VimarComponent, action_type: ActionType, *args):
        """Send a request coming from HomeAssistant to Gateway."""
        try:
            self.client.send(component, action_type, *args)
        except WebSocketConnectionClosedException:
            self.start()

    def update_data(self):
        """Update data when new status is received from the Gateway."""
        self.hass.add_job(self._update_data)

    @callback
    def _update_data(self):
        data = self.client.retrieve_data(self.options)
        self.async_set_updated_data(data)

    async def _async_update_data(self) -> VimarData:
        return self.client.retrieve_data(self.options)

    def _get_gateway_info(self, user_input: dict[str, str]) -> GatewayInfo:
        return GatewayInfo(
            host=user_input[HOST],
            address=user_input[ADDRESS],
            port=user_input[PORT],
            deviceuid=user_input[GATEWAY_ID],
            plantname=user_input[GATEWAY_NAME],
            protocolversion=user_input[PROTOCOL],
        )
