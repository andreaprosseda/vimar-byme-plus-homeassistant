"""Platform for button integration."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_button import VimarButton
from .vimar.model.enum.action_type import ActionType
from .vimar.utils.logger import log_debug, log_info


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

    @callback
    def _handle_coordinator_update(self) -> None:
        super()._handle_coordinator_update()

        if self._component and self._component.executed:
            event = {
                "id": self._component.id,
                "name": self._component.name,
                "type": "scene_executed",
            }
            self.hass.bus.fire("vimar_byme_plus_event", event)
            log_debug(__name__, f"Event fired by {self._component.name}")
