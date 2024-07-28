"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DATA_COORDINATOR, DATA_UNDO_UPDATE_LISTENER, DOMAIN
from .coordinator import VimarDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.COVER, Platform.LIGHT]
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Vimar integration."""
    _LOGGER.debug("async_setup started")
    hass.data.setdefault(DOMAIN, {})

    if hass.config_entries.async_entries(DOMAIN):
        return True
    context = {"source": SOURCE_IMPORT}
    data = config[DOMAIN]

    if data.get("username"):
        hass.async_create_task(
            hass.config_entries.flow.async_init(DOMAIN, context=context, data=data)
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vimar from a config entry."""
    _LOGGER.debug("async_setup_entry started")
    if not entry.options:
        options = {"username": "usr", "password": "psw"}
        hass.config_entries.async_update_entry(entry, options=options)

    coordinator = VimarDataUpdateCoordinator(hass, entry.options)
    await coordinator.start()
    await coordinator.async_config_entry_first_refresh()

    undo_listener = entry.add_update_listener(_async_update_listener)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_COORDINATOR: coordinator,
        DATA_UNDO_UPDATE_LISTENER: undo_listener,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry started")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN][entry.entry_id][DATA_UNDO_UPDATE_LISTENER]()
        await hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR].stop()
        hass.data[DOMAIN].pop(entry.entry_id)
        hass.data.pop(DOMAIN)

    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.debug("_async_update_listener started")
    await hass.config_entries.async_reload(entry.entry_id)
