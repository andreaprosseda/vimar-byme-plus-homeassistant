"""Provides the Vimar Coordinator."""

import logging

from websocket import WebSocketConnectionClosedException
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import ADDRESS, CODE, DOMAIN, GATEWAY_ID, GATEWAY_NAME, HOST, PORT, PROTOCOL
from .vimar.client.vimar_client import VimarClient
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.action_type import ActionType
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.gateway.vimar_data import VimarData

_LOGGER = logging.getLogger(__name__)


class Coordinator(DataUpdateCoordinator[VimarData]):
    """Vimar coordinator."""

    gateway_info: GatewayInfo
    client: VimarClient

    def __init__(self, hass: HomeAssistant, user_input: dict[str, str]) -> None:
        """Initialize the coordinator."""
        self.gateway_info = self._get_gateway_info(user_input)
        self.client = VimarClient(self.gateway_info, self.update_data)
        self.client.set_setup_code(user_input.get(CODE))

        super().__init__(hass, _LOGGER, name=DOMAIN)

    def associate(self):
        """Test coordinator processes."""
        self.client.association_phase()

    def start(self):
        """Start coordinator processes."""
        self.client.operational_phase()
        self._update_data()

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
        self.hass.loop.call_soon_threadsafe(self._update_data)

    def _update_data(self):
        data = self.client.retrieve_data()
        self.async_set_updated_data(data)

    async def _async_update_data(self) -> VimarData:
        return self.client.retrieve_data()

    def _get_gateway_info(self, user_input: dict[str, str]) -> GatewayInfo:
        return GatewayInfo(
            host=user_input[HOST],
            address=user_input[ADDRESS],
            port=user_input[PORT],
            deviceuid=user_input[GATEWAY_ID],
            plantname=user_input[GATEWAY_NAME],
            protocolversion=user_input[PROTOCOL],
        )
