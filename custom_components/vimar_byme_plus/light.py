"""Platform for light integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import VimarDataUpdateCoordinator
from .middleware.vimar_entity import VimarEntity
from .vimar.model.enum.component_type import ComponentType
from .vimar.model.repository.user_component import UserComponent
from .vimar.utils.logger import log_debug

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator: VimarDataUpdateCoordinator = entry.runtime_data
    components = coordinator.get_components(ComponentType.LIGHT)
    entities = [VimarLight(coordinator, component) for component in components]
    async_add_entities(entities, True)


class VimarLight(VimarEntity, LightEntity):
    """Provides a Vimar light."""

    def __init__(
        self, coordinator: VimarDataUpdateCoordinator, component: UserComponent
    ) -> None:
        """Initialize the light."""
        VimarEntity.__init__(self, coordinator, component)

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on."""
        return self.get_element("SFE_State_OnOff") == "On"

    @property
    def brightness(self) -> int | None:
        """Return Brightness of this light between 0..255."""
        return 255

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        """Return RGB colors."""
        return None

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation."""
        return None

    @property
    def color_mode(self) -> ColorMode:
        """Return the color mode of the light."""
        return ColorMode.ONOFF

    @property
    def supported_color_modes(self) -> set[ColorMode]:
        """Flag supported color modes."""
        return {self.color_mode}

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the Vimar light on."""
        # await self._device.set_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        # await self._device.set_off()
