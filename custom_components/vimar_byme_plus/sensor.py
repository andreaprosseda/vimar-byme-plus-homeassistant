"""Platform for sensor integration."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.components.sensor.const import SensorStateClass, UNIT_CONVERTERS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_sensor import VimarSensor
from .vimar.utils.logger import log_info


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


class Sensor(BaseEntity, SensorEntity):
    """Provides a Vimar Sensor."""

    _component: VimarSensor
    temp_measure: dict
    previous_measure: dict
    current_measure: dict

    def __init__(self, coordinator: Coordinator, component: VimarSensor) -> None:
        """Initialize the sensor."""
        self._component = component
        self.temp_measure = self._create_measure()
        self.previous_measure = self._create_measure()
        self.current_measure = self._create_measure(component)
        BaseEntity.__init__(self, coordinator, component)

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
            return self._compute_energy()
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
        self.temp_measure = self.current_measure.copy()
        super()._handle_coordinator_update()
        self._update_measures()

    def _compute_energy(self) -> str | Decimal | None:
        current_date = self.current_measure.get("date")
        previous_date = self.previous_measure.get("date")
        current_power = self.current_measure.get("value")
        previous_power = self.previous_measure.get("value")
        interval = self._delta_time_in_hours(current_date, previous_date)
        if not previous_power and not current_power:
            return None
        if not previous_power or not interval:
            return current_power
        return ((current_power + previous_power) / 2) * interval

    def _delta_time_in_hours(self, t1: datetime, t2: datetime) -> Decimal | None:
        if not t1 or not t2:
            return None
        seconds_in_hour = 3600
        delta_seconds = (t1 - t2).total_seconds()
        if not delta_seconds:
            return None
        return Decimal(delta_seconds / seconds_in_hour)

    def _update_measures(self):
        self.current_measure = self._create_measure(self._component)
        if self._can_update_previous_measure():
            self.previous_measure = self.temp_measure.copy()
        self.temp_measure = None

    def _can_update_previous_measure(self) -> bool:
        temp_date: datetime = self.temp_measure.get("date")
        current_date: datetime = self.current_measure.get("date")
        if temp_date and current_date:
            return (current_date - temp_date).total_seconds() > 0
        return False

    def _create_measure(self, component: VimarSensor | None = None) -> dict:
        if not component or not component.native_value:
            return {}
        return {"value": component.native_value, "date": component.last_update}
