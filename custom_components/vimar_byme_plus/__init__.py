"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import SOURCE_REAUTH, ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .const import CODE
from .coordinator import Coordinator
from .vimar.utils.logger import log_debug
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException
from .vimar.utils.logger import log_info

PLATFORMS = [Platform.CLIMATE, Platform.COVER, Platform.LIGHT]

type CoordinatorConfigEntry = ConfigEntry[Coordinator]


async def async_setup_entry(hass: HomeAssistant, entry: CoordinatorConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    coordinator = Coordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    coordinator.initialize(entry.data)
    await start(coordinator)
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: CoordinatorConfigEntry
) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        entry.runtime_data.stop()

    return unload_ok


async def start(coordinator: Coordinator):
    """Start the coordinator process."""
    try:
        coordinator.start()
    except VimarErrorResponseException as err:
        raise ConfigEntryAuthFailed(err) from err
    except CodeNotValidException as err:
        raise ConfigEntryAuthFailed(err) from err
