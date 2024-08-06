"""Platform for cover integration."""

from __future__ import annotations

import logging
from typing import Any

from xknx import XKNX
from xknx.devices import Cover

from homeassistant.components.cover import (
    ATTR_POSITION,
    ATTR_TILT_POSITION,
    CoverEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import VimarDataUpdateCoordinator
from .vimar.model.vimar_application import VimarApplication, VimarType
from .vimar.enum.vimar_dpt_values import DptValue
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
    covers = coordinator.config.get_entities(VimarType.COVER)
    doors = coordinator.config.get_entities(VimarType.DOOR)
    apps = covers + doors
    entities = [VimarCover(coordinator, app) for app in apps]
    _LOGGER.debug("Lights found: %s", len(entities))
    async_add_entities(entities, True)


class VimarCover(VimarEntity, CoverEntity):
    """Provides a Vimar cover."""

    _device: Cover

    def __init__(
        self, coordinator: VimarDataUpdateCoordinator, app: VimarApplication
    ) -> None:
        """Initialize the light."""
        VimarEntity.__init__(self, coordinator, app)
        self._device = self._register_knx_device(coordinator.knx)

    @property
    def current_cover_position(self) -> int | None:
        """Return the current position of the cover.

        None is unknown, 0 is closed, 100 is fully open.
        """
        # In KNX 0 is open, 100 is closed.
        if (pos := self._device.current_position()) is not None:
            return 100 - pos
        return None

    @property
    def is_closed(self) -> bool | None:
        """Return if the cover is closed."""
        # state shall be "unknown" when xknx travelcalculator is not initialized
        if self._device.current_position() is None:
            return None
        return self._device.is_closed()

    @property
    def is_opening(self) -> bool:
        """Return if the cover is opening or not."""
        return self._device.is_opening()

    @property
    def is_closing(self) -> bool:
        """Return if the cover is closing or not."""
        return self._device.is_closing()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        await self._device.set_down()

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        await self._device.set_up()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Move the cover to a specific position."""
        knx_position = 100 - kwargs[ATTR_POSITION]
        await self._device.set_position(knx_position)

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
        await self._device.stop()

    @property
    def current_cover_tilt_position(self) -> int | None:
        """Return current tilt position of cover."""
        if (angle := self._device.current_angle()) is not None:
            return 100 - angle
        return None

    async def async_set_cover_tilt_position(self, **kwargs: Any) -> None:
        """Move the cover tilt to a specific position."""
        knx_tilt_position = 100 - kwargs[ATTR_TILT_POSITION]
        await self._device.set_angle(knx_tilt_position)

    async def async_open_cover_tilt(self, **kwargs: Any) -> None:
        """Open the cover tilt."""
        if self._device.angle.writable:
            await self._device.set_angle(0)
        else:
            await self._device.set_short_up()

    async def async_close_cover_tilt(self, **kwargs: Any) -> None:
        """Close the cover tilt."""
        if self._device.angle.writable:
            await self._device.set_angle(100)
        else:
            await self._device.set_short_down()

    async def async_stop_cover_tilt(self, **kwargs: Any) -> None:
        """Stop the cover tilt."""
        await self._device.stop()

    def _register_knx_device(self, knx: XKNX) -> Cover:
        cover = None
        if self.type == VimarType.COVER:
            cover = self._get_cover(knx)
        if self.type == VimarType.DOOR:
            cover = self._get_door(knx)
        knx.devices.add(cover)
        return cover

    def _get_cover(self, knx: XKNX) -> Cover:
        return Cover(
            knx,
            name=self.app.label,
            group_address_long=self._get_address(DptValue.MOVE_LONG),
            group_address_position=self._get_address(DptValue.POSITION),
            group_address_position_state=self._get_address(DptValue.POSITION_STATE),
            group_address_stop=self._get_address(DptValue.STOP),
            travel_time_down=30,
            travel_time_up=30,
            invert_updown=False,
        )

    def _get_door(self, knx: XKNX) -> Cover:
        return Cover(
            knx,
            name=self.app.label,
            group_address_long=self._get_address(DptValue.ON_OFF),
            travel_time_down=1,
            travel_time_up=0,
            invert_updown=True,
        )
