"""Platform for binary sensor integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_binary_sensor import VimarBinarySensor
from .vimar.utils.logger import log_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_binary_sensors()
    entities = [BinarySensor(coordinator, component) for component in components]
    log_info(__name__, f"Binary Sensors found: {len(entities)}")
    async_add_entities(entities, True)


class BinarySensor(BaseEntity, BinarySensorEntity):
    """Provides a Vimar Binary Sensor."""

    _component: VimarBinarySensor
    temp_measure: dict
    previous_measure: dict
    current_measure: dict

    def __init__(self, coordinator: Coordinator, component: VimarBinarySensor) -> None:
        """Initialize the binary sensor."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        """Return the class of this entity."""
        return self._component.device_class

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._component.is_on
