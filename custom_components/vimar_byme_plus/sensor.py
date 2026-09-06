"""Platform for sensor integration."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
)
from homeassistant.components.sensor.const import UNIT_CONVERTERS, SensorStateClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import StateType
from homeassistant.util import dt as dt_util

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_sensor import VimarSensor
from .vimar.utils.logger import log_info

# Il gateway Vimar invia `changestatus` solo quando un valore CAMBIA. Con un
# carico stabile l'elemento della potenza non viene riscritto per ore, e
# un'integrazione guidata dai soli aggiornamenti del gateway accumula zero
# energia in tutto quel tempo (issue #79). Ad ogni tick l'integrazione riparte
# dal punto in cui si era fermata usando l'ultima potenza nota: e' lo stesso
# meccanismo del sensore `integration` di Home Assistant con `max_sub_interval`.
_ENERGY_SUB_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_sensors()
    entities = [Sensor(coordinator, component) for component in components]
    log_info(__name__, f"Sensors found: {len(entities)}")
    async_add_entities(entities, True)


class Sensor(BaseEntity, RestoreSensor):
    """Provides a Vimar Sensor.

    For sensors with `device_class=ENERGY` the integration receives raw
    instantaneous power readings from the gateway and integrates them
    over time (trapezoidal rule) into a cumulative kWh counter.
    The cumulative is persisted via `RestoreSensor` so it survives HA
    restarts and avoids the spurious counter resets that previously
    triggered HA's `total_increasing` warnings (issue #25).
    """

    _component: VimarSensor
    previous_measure: dict
    _running_total: Decimal | None

    def __init__(self, coordinator: Coordinator, component: VimarSensor) -> None:
        """Initialize the sensor."""
        self._component = component
        self.previous_measure = self._create_measure(component)
        self._running_total = None
        BaseEntity.__init__(self, coordinator, component)

    async def async_added_to_hass(self) -> None:
        """Restore the running total for ENERGY sensors across restarts."""
        await super().async_added_to_hass()
        if self.device_class != SensorDeviceClass.ENERGY:
            return
        last = await self.async_get_last_sensor_data()
        if last is not None and last.native_value is not None:
            try:
                self._running_total = Decimal(str(last.native_value))
            except (TypeError, ValueError, ArithmeticError):
                self._running_total = None
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self._async_energy_tick, _ENERGY_SUB_INTERVAL
            )
        )

    @callback
    def _async_energy_tick(self, _now: datetime) -> None:
        """Integrate the power already known up to this instant.

        Without this the counter only advances when the gateway happens to
        send a new reading, so a load that stays perfectly stable produces a
        flat energy sensor (issue #79).
        """
        if not self.available:
            return
        if self._accumulate_energy():
            self.async_write_ha_state()

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the class of this entity."""
        return self._component.device_class

    @property
    def state_class(self) -> SensorStateClass | str | None:
        """Return the state class of this entity, if any."""
        return self._component.state_class

    @property
    def options(self) -> list[str] | None:
        """Return a set of possible options."""
        return self._component.options

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the value reported by the sensor."""
        if self.device_class == SensorDeviceClass.ENERGY:
            return self._running_total
        return self._component.native_value

    @property
    def suggested_display_precision(self) -> int | None:
        """Return the suggested number of decimal digits for display."""
        return self._component.decimal_precision

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor, if any."""
        return self._component.unit_of_measurement

    @property
    def suggested_unit_of_measurement(self) -> str | None:
        """Return the unit which should be used for the sensor's state."""
        has_converter = UNIT_CONVERTERS.get(self.device_class) is not None
        return self._component.unit_of_measurement if has_converter else None

    @callback
    def _handle_coordinator_update(self) -> None:
        super()._handle_coordinator_update()
        # `super()` has already published the state, with the total as it was
        # BEFORE this reading was integrated. Publishing again is what makes
        # the new total visible; without it the energy sensor always lagged
        # one update behind.
        if self._accumulate_energy():
            self.async_write_ha_state()

    def _accumulate_energy(self) -> bool:
        """Integrate the latest power reading into the cumulative kWh total.

        Returns True when the running total actually grew.
        """
        if self.device_class != SensorDeviceClass.ENERGY:
            return False
        current = self._create_measure(self._component)
        if not current:
            return False
        previous = self.previous_measure
        # The anchor ALWAYS moves forward on a valid reading, before any other
        # decision. It used to move only on the happy path, and one unusable
        # anchor was enough to freeze the counter for good: at startup the
        # component comes from `sfdiscovery`, which carries no timestamp, so
        # the anchor was born with `date=None`; every later reading then hit
        # the `interval is None` branch and returned WITHOUT replacing it.
        # The energy sensors stopped at the value restored on boot and never
        # moved again — the "0.00000 kWh" of issue #79.
        self.previous_measure = current
        if not previous:
            return False  # first reading: nothing to integrate against yet
        interval = self._delta_time_in_hours(current.get("date"), previous.get("date"))
        if interval is None or interval <= 0:
            return False
        increment = self._compute_energy_increment(current, previous, interval)
        if increment is None or increment <= 0:
            return False
        base = self._running_total if self._running_total is not None else Decimal(0)
        self._running_total = base + increment
        return True

    def _compute_energy_increment(
        self, current: dict, previous: dict, interval: Decimal
    ) -> Decimal | None:
        """Energy delivered in the interval (trapezoidal rule): avg(P) * dt."""
        current_power = current.get("value")
        previous_power = previous.get("value")
        if current_power is None or previous_power is None:
            return None
        try:
            current_d = Decimal(str(current_power))
            previous_d = Decimal(str(previous_power))
        except (TypeError, ValueError, ArithmeticError):
            return None
        return ((current_d + previous_d) / 2) * interval

    def _delta_time_in_hours(self, t1: datetime, t2: datetime) -> Decimal | None:
        if not t1 or not t2:
            return None
        seconds_in_hour = 3600
        delta_seconds = (t1 - t2).total_seconds()
        if not delta_seconds:
            return None
        return Decimal(delta_seconds / seconds_in_hour)

    def _create_measure(self, component: VimarSensor | None = None) -> dict:
        """Anchor point for the integration: a power and the instant it holds from.

        Two details that were wrong before, both of them silent:

        - `not component.native_value` also discarded a reading of exactly
          zero, because `Decimal("0.000")` is falsy. A load that switches off
          therefore never moved the anchor, and the first reading after the
          pause integrated the WHOLE pause at the power the load had before
          switching off — the overestimate reported in issue #79.
        - the instant came from the gateway element's own timestamp, which
          stands still while the reading does not change. Wall-clock time is
          what energy actually accrues against, so the anchor uses that.
          `dt_util.utcnow()` and not `datetime.now()`: a naive local clock
          would gain or lose an hour of energy at every DST change.
        """
        if component is None or component.native_value is None:
            return {}
        return {"value": component.native_value, "date": dt_util.utcnow()}
