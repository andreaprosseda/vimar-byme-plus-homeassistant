"""Provides the Vimar Coordinator."""

from collections.abc import Callable
from datetime import datetime, timedelta
import logging

from websocket import WebSocketConnectionClosedException

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import ADDRESS, CODE, DOMAIN, GATEWAY_ID, GATEWAY_NAME, HOST, PORT, PROTOCOL
from .vimar.client.vimar_client import VimarClient
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.action_type import ActionType
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.gateway.vimar_data import VimarData

_LOGGER = logging.getLogger(__name__)

# Watchdog tick frequency. The Vimar gateway pushes events on activity;
# in idle moments the keep-alive (~90s) is the only traffic. A 5-minute
# stale window is well above that, so a healthy connection never trips
# the watchdog while a silent-stale one is detected within at most 10
# minutes (one watchdog tick after crossing the threshold).
_WATCHDOG_INTERVAL = timedelta(minutes=5)
_STALE_THRESHOLD_SECONDS = 300


class Coordinator(DataUpdateCoordinator[VimarData]):
    """Vimar coordinator."""

    gateway_info: GatewayInfo
    client: VimarClient

    def __init__(self, hass: HomeAssistant, user_input: dict[str, str]) -> None:
        """Initialize the coordinator."""
        self.gateway_info = self._get_gateway_info(user_input)
        self.client = VimarClient(self.gateway_info, self.update_data)
        self.client.set_setup_code(user_input.get(CODE))
        self._unsub_watchdog: Callable[[], None] | None = None

        super().__init__(hass, _LOGGER, name=DOMAIN)

    def associate(self):
        """Test coordinator processes."""
        self.client.association_phase()

    def start(self):
        """Start coordinator processes."""
        self.client.operational_phase()
        self.update_data()
        self._setup_watchdog()

    def stop(self):
        """Stop coordinator processes."""
        self._teardown_watchdog()
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
        data = self.client.retrieve_data()
        self.async_set_updated_data(data)

    async def _async_update_data(self) -> VimarData:
        return self.client.retrieve_data()

    # --- Watchdog -----------------------------------------------------
    # The integration relies on a daemon thread (`VimarServiceThread`)
    # for the gateway WebSocket loop. If that thread dies — or the
    # broker stops sending messages without closing the TCP — there is
    # no internal mechanism to detect it: HA keeps reading stale data
    # from the local DB. The watchdog runs on the HA event loop and
    # forces a reconnect in either case.

    def _setup_watchdog(self) -> None:
        if self._unsub_watchdog is not None:
            return
        self._unsub_watchdog = async_track_time_interval(
            self.hass, self._watchdog_tick, _WATCHDOG_INTERVAL
        )

    def _teardown_watchdog(self) -> None:
        if self._unsub_watchdog is not None:
            self._unsub_watchdog()
            self._unsub_watchdog = None

    async def _watchdog_tick(self, _now: datetime) -> None:
        alive = self.client.is_thread_alive()
        stale_seconds = self.client.seconds_since_last_message
        if alive and stale_seconds < _STALE_THRESHOLD_SECONDS:
            return
        _LOGGER.warning(
            "Vimar watchdog tripped (thread_alive=%s, stale=%.0fs); reconnecting",
            alive,
            stale_seconds,
        )
        await self.hass.async_add_executor_job(self.client.reconnect)

    def _get_gateway_info(self, user_input: dict[str, str]) -> GatewayInfo:
        return GatewayInfo(
            host=user_input[HOST],
            address=user_input[ADDRESS],
            port=user_input[PORT],
            deviceuid=user_input[GATEWAY_ID],
            plantname=user_input[GATEWAY_NAME],
            protocolversion=user_input[PROTOCOL],
        )
