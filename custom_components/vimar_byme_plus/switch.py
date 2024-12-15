"""Platform for switch integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_switch import VimarSwitch
from .vimar.model.enum.action_type import ActionType
from .vimar.utils.logger import log_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_switches()
    entities = [Switch(coordinator, component) for component in components]
    log_info(__name__, f"Switches found: {len(entities)}")
    async_add_entities(entities, True)


class Switch(BaseEntity, SwitchEntity):
    """Provides a Vimar switch."""

    _component: VimarSwitch

    def __init__(self, coordinator: Coordinator, component: VimarSwitch) -> None:
        """Initialize the switch."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on."""
        return self._component.is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the Vimar switch on."""
        self.send(ActionType.ON)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self.send(ActionType.OFF)
