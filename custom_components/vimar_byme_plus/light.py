"""Platform for light integration."""

from __future__ import annotations

import logging
from typing import Any

from xknx import XKNX
from xknx.devices import Light

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import VimarDataUpdateCoordinator
from .vimar.vimar_application import VimarApplication, VimarType
from .vimar.vimar_dpt_values import DptValue
from .vimar.vimar_entity import VimarEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    hass_entry = hass.data[DOMAIN][entry.entry_id]
    coordinator: VimarDataUpdateCoordinator = hass_entry[DATA_COORDINATOR]
    apps = coordinator.config.get_entities(VimarType.LIGHT)
    entities = [VimarLight(coordinator, app) for app in apps]
    _LOGGER.debug("Lights found: %s", len(entities))
    async_add_entities(entities, True)


class VimarLight(VimarEntity, LightEntity):
    """Provides a Vimar light."""

    _device: Light

    def __init__(
        self, coordinator: VimarDataUpdateCoordinator, app: VimarApplication
    ) -> None:
        """Initialize the light."""
        VimarEntity.__init__(self, coordinator, app)
        self._device = self._register_knx_device(coordinator.knx)

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on."""
        return self._device.state is True

    @property
    def brightness(self) -> int | None:
        """Return Brightness of this light between 0..255."""
        return self._device.brightness

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        """Return RGB colors."""
        return self._device.rgbw

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation."""
        return self._device.current_hs_color

    @property
    def color_mode(self) -> ColorMode:
        """Return the color mode of the light."""
        if self._device.supports_xyy_color:
            return ColorMode.XY
        if self._device.supports_hs_color:
            return ColorMode.HS
        if self._device.supports_rgbw:
            return ColorMode.RGBW
        if self._device.supports_color:
            return ColorMode.RGB
        if (
            self._device.supports_color_temperature
            or self._device.supports_tunable_white
        ):
            return ColorMode.COLOR_TEMP
        if self._device.supports_brightness:
            return ColorMode.BRIGHTNESS
        return ColorMode.ONOFF

    @property
    def supported_color_modes(self) -> set[ColorMode]:
        """Flag supported color modes."""
        return {self.color_mode}

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the Vimar light on."""
        await self._device.set_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self._device.set_off()

    def _register_knx_device(self, knx: XKNX) -> Light:
        light = Light(
            knx,
            name=self.app.label,
            group_address_switch=self._get_address(DptValue.ON_OFF),
            group_address_switch_state=self._get_address(DptValue.ON_OFF_STATE),
        )
        knx.devices.add(light)
        return light
