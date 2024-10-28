"""Platform for cover integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import Coordinator
from . import CoordinatorConfigEntry
from .vimar.model.component.vimar_cover import VimarCover
from .vimar.utils.logger import log_debug
from .base_entity import BaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_covers()
    entities = [Cover(coordinator, component) for component in components]
    log_debug(__name__, f"Covers found: {len(entities)}")
    async_add_entities(entities, True)


class Cover(BaseEntity, CoverEntity):
    """Provides a Vimar Cover."""

    _component: VimarCover

    def __init__(self, coordinator: Coordinator, component: VimarCover) -> None:
        """Initialize the cover."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def current_cover_position(self) -> int | None:
        """Return current position of cover.

        HomeAssistantDescription: The current position of cover where 0 means closed and 100 is fully open.
        """
        position = self._component.current_cover_position
        return 100 - position if position else None

    @property
    def is_opening(self) -> bool | None:
        """Return if the cover is opening or not.

        HomeAssistantDescription: If the cover is opening or not. Used to determine state.
        """
        return self._component.is_opening

    @property
    def is_closing(self) -> bool | None:
        """Return if the cover is closing or not.

        HomeAssistantDescription: If the cover is closing or not. Used to determine state.
        """
        return self._component.is_closing

    @property
    def is_closed(self) -> bool | None:
        """Return if the cover is closed or not.

        HomeAssistantDescription: If the cover is closed or not. Used to determine state.
        """
        return self._component.is_closed

    def open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""

    def close_cover(self, **kwargs: Any) -> None:
        """Close cover."""

    def set_cover_position(self, **kwargs: Any) -> None:
        """Move the cover to a specific position."""

    def stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
