"""Platform for sensor integration."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.components.sensor.const import SensorStateClass
from homeassistant.core import HomeAssistant
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

    def __init__(self, coordinator: Coordinator, component: VimarSensor) -> None:
        """Initialize the cover."""
        self._component = component
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
        return self._component.unit_of_measurement
