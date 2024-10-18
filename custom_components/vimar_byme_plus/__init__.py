"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import VimarDataUpdateCoordinator
from .vimar.utils.logger import log_debug

PLATFORMS: list[Platform] = [
    Platform.LIGHT,
    # Platform.CLIMATE,
    Platform.COVER
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vimar from a config entry."""
    log_debug(__name__, "Method 'async_setup_entry' started")
    coordinator = VimarDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    await coordinator.start()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    log_debug(__name__, "Method 'async_unload_entry' started")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: VimarDataUpdateCoordinator = entry.runtime_data
        coordinator.stop()
    return unload_ok
