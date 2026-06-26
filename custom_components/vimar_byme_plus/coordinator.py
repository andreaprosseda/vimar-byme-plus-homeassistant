"""Provides the Vimar Coordinator."""

from collections.abc import Callable
from datetime import datetime, timedelta
import logging

from websocket import WebSocketConnectionClosedException

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
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
    SECTION_REALTIME,
    SECTION_TILT_TOLERANCE,
)
from .vimar.client.vimar_client import VimarClient
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.action_type import ActionType
from .vimar.model.gateway.gateway_info import GatewayInfo
from .vimar.model.gateway.vimar_data import VimarData
from .vimar.model.integration_options import IntegrationOptions

_LOGGER = logging.getLogger(__name__)

# Watchdog tick frequency. The Vimar gateway pushes events on activity;
# in idle moments the keep-alive (~90s) is the only traffic. A 5-minute
# stale window is well above that, so a healthy connection never trips
# the watchdog while a silent-stale one is detected within at most 10
# minutes (one watchdog tick after crossing the threshold).
_WATCHDOG_INTERVAL = timedelta(minutes=5)
_STALE_THRESHOLD_SECONDS = 300

# Substring used by every "Aggiornamenti RealTime" button id, regardless
# of whether it was produced by a sensor or energy mapper.
_REALTIME_BUTTON_MARKER = "real_time"


class Coordinator(DataUpdateCoordinator[VimarData]):
    """Vimar coordinator."""

    gateway_info: GatewayInfo
    client: VimarClient

    def __init__(
        self,
        hass: HomeAssistant,
        user_input: dict[str, str],
        entry: ConfigEntry | None = None,
    ) -> None:
        """Initialize the coordinator."""
        self._entry = entry
        self.gateway_info = self._get_gateway_info(user_input)
        self.client = VimarClient(self.gateway_info, self.update_data)
        self.client.set_setup_code(user_input.get(CODE))
        self._unsub_watchdog: Callable[[], None] | None = None
        self._unsub_realtime: list[Callable[[], None]] = []

        super().__init__(hass, _LOGGER, name=DOMAIN, config_entry=entry)

    @property
    def options(self) -> IntegrationOptions:
        """Materialise entry.options into the runtime options bundle."""
        if self._entry is None:
            return IntegrationOptions()
        raw = self._entry.options or {}
        return IntegrationOptions(
            counter_types=raw.get(SECTION_COUNTERS, {}) or {},
            realtime_intervals=raw.get(SECTION_REALTIME, {}) or {},
            tilt_tolerance=int(raw.get(SECTION_TILT_TOLERANCE, 0) or 0),
        )

    def associate(self):
        """Test coordinator processes."""
        self.client.association_phase()

    def start(self):
        """Start coordinator processes."""
        self.client.operational_phase()
        self.update_data()
        self._setup_watchdog()
        self._setup_realtime()

    def stop(self):
        """Stop coordinator processes."""
        self._teardown_realtime()
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
        data = self.client.retrieve_data(self.options)
        self.async_set_updated_data(data)

    async def _async_update_data(self) -> VimarData:
        return self.client.retrieve_data(self.options)

    # --- Watchdog -----------------------------------------------------

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

    # --- Realtime auto-press -----------------------------------------
    # Per-device timers configured via OptionsFlow → SECTION_REALTIME.
    # Each entry maps a Vimar device idsf (as string) to an interval in
    # seconds; on every tick the corresponding "Aggiornamenti RealTime"
    # button is pressed, which routes to the existing action handlers
    # and emits SFE_Cmd_TimedDynamicMode = "Start" on the gateway.

    def _setup_realtime(self) -> None:
        self._teardown_realtime()
        for main_id_str, raw_interval in self.options.realtime_intervals.items():
            try:
                seconds = int(raw_interval)
            except (TypeError, ValueError):
                continue
            if seconds <= 0:
                continue
            unsub = async_track_time_interval(
                self.hass,
                self._make_realtime_callback(str(main_id_str)),
                timedelta(seconds=seconds),
            )
            self._unsub_realtime.append(unsub)

    def _teardown_realtime(self) -> None:
        for unsub in self._unsub_realtime:
            unsub()
        self._unsub_realtime = []

    def _make_realtime_callback(self, main_id_str: str) -> Callable[[datetime], None]:
        async def _cb(_now: datetime) -> None:
            await self._fire_realtime_press(main_id_str)

        return _cb

    async def _fire_realtime_press(self, main_id_str: str) -> None:
        if self.data is None:
            return
        target = next(
            (
                b
                for b in self.data.get_buttons()
                if _REALTIME_BUTTON_MARKER in str(b.id)
                and str(b.main_id) == main_id_str
            ),
            None,
        )
        if target is None:
            _LOGGER.debug(
                "Realtime tick: no button found for main_id=%s (skipping)",
                main_id_str,
            )
            return
        await self.hass.async_add_executor_job(self._send_realtime_press, target)

    def _send_realtime_press(self, button: VimarComponent) -> None:
        try:
            self.client.send(button, ActionType.PRESS)
        except Exception as exc:  # pylint: disable=broad-except
            _LOGGER.warning("Realtime auto-press failed for %s: %r", button.id, exc)

    def _get_gateway_info(self, user_input: dict[str, str]) -> GatewayInfo:
        return GatewayInfo(
            host=user_input[HOST],
            address=user_input[ADDRESS],
            port=user_input[PORT],
            deviceuid=user_input[GATEWAY_ID],
            plantname=user_input[GATEWAY_NAME],
            protocolversion=user_input[PROTOCOL],
        )
