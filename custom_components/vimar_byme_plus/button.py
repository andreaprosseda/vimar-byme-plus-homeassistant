"""Platform for button integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_button import VimarButton
from .vimar.model.enum.action_type import ActionType
from .vimar.utils.logger import log_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_buttons()
    entities = [Button(coordinator, component) for component in components]
    log_info(__name__, f"Buttons found: {len(entities)}")
    async_add_entities(entities, True)


class Button(BaseEntity, ButtonEntity):
    """Provides a Vimar button."""

    _component: VimarButton

    def __init__(self, coordinator: Coordinator, component: VimarButton) -> None:
        """Initialize the button."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    def press(self) -> None:
        """Press the button."""
        self.send(ActionType.PRESS)
