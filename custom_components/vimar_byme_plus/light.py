"""Platform for light integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base_entity import BaseEntity
from . import CoordinatorConfigEntry
from .coordinator import Coordinator
from .vimar.model.component.vimar_light import VimarLight
from .vimar.utils.logger import log_debug

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_lights()
    entities = [Light(coordinator, component) for component in components]
    log_debug(__name__, f"Lights found: {len(entities)}")
    async_add_entities(entities, True)


class Light(BaseEntity, LightEntity):
    """Provides a Vimar light."""

    _component: VimarLight

    def __init__(self, coordinator: Coordinator, component: VimarLight) -> None:
        """Initialize the light."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on.

        HomeAssistant Description: If the light entity is on or not.
        """
        return self._component.is_on

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light.

        HomeAssitant Description: The brightness of this light between 1..255.
        """
        brightness = self._component.brightness
        return brightness * 255 / 100 if brightness else None

    @property
    def color_mode(self) -> ColorMode | str | None:
        """Return the color mode of the light.

        HomeAssitant Description: The color mode of the light. The returned color mode must be present in the supported_color_modes property unless the light is rendering an effect.
        """
        return self._component.color_mode.value

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation color value [float, float].

        HomeAssitant Description: The hue and saturation color value (float, float). This property will be copied to the light's state attribute when the light's color mode is set to ColorMode.HS and ignored otherwise.
        """
        return self._component.hs_color

    @property
    def xy_color(self) -> tuple[float, float] | None:
        """Return the xy color value [float, float].

        HomeAssitant Description: The xy color value (float, float). This property will be copied to the light's state attribute when the light's color mode is set to ColorMode.XY and ignored otherwise.
        """
        return self._component.xy_color

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        """Return the rgb color value [int, int, int].

        HomeAssitant Description: The rgb color value (int, int, int). This property will be copied to the light's state attribute when the light's color mode is set to ColorMode.RGB and ignored otherwise.
        """
        return self._component.rgb_color

    @property
    def rgbw_color(self) -> tuple[int, int, int, int] | None:
        """Return the rgbw color value [int, int, int, int].

        HomeAssitant Description: The rgbw color value (int, int, int, int). This property will be copied to the light's state attribute when the light's color mode is set to ColorMode.RGBW and ignored otherwise.
        """
        return self._component.rgbw_color

    @property
    def rgbww_color(self) -> tuple[int, int, int, int, int] | None:
        """Return the rgbww color value [int, int, int, int, int].

        HomeAssitant Description: The rgbww color value (int, int, int, int, int). This property will be copied to the light's state attribute when the light's color mode is set to ColorMode.RGBWW and ignored otherwise.
        """
        return self._component.rgbww_color

    @property
    def effect_list(self) -> list[str] | None:
        """Return the list of supported effects.

        HomeAssitant Description: The list of supported effects.
        """
        return self._component.effect_list

    @property
    def effect(self) -> str | None:
        """Return the current effect.

        HomeAssitant Description: The current effect. Should be EFFECT_OFF if the light supports effects and no effect is currently rendered.
        """
        return self._component.effect

    @property
    def supported_color_modes(self) -> set[ColorMode] | set[str] | None:
        """Flag supported color modes.

        HomeAssitant Description: Flag supported color modes.
        """
        modes = self._component.supported_color_modes
        return {mode.value for mode in modes}

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the Vimar light on."""
        # await self._component.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        # await self._component.turn_off()
