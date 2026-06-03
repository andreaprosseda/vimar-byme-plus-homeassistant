"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError

from .const import DOMAIN, GATEWAY_ID
from .coordinator import Coordinator
from .vimar.database.database import Database
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.COVER,
    Platform.LIGHT,
    Platform.MEDIA_PLAYER,
    Platform.SENSOR,
    Platform.SWITCH,
]

type CoordinatorConfigEntry = ConfigEntry[Coordinator]

SERVICE_RESTART = "restart"
ATTR_ENTRY_ID = "entry_id"
RESTART_SERVICE_SCHEMA = vol.Schema(
    {vol.Optional(ATTR_ENTRY_ID): str}
)


async def async_setup_entry(hass: HomeAssistant, entry: CoordinatorConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    coordinator = Coordinator(hass, entry.data, entry)
    await coordinator.async_config_entry_first_refresh()
    await start(coordinator)
    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _async_register_restart_service(hass)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: CoordinatorConfigEntry
) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        entry.runtime_data.stop()
    entry.runtime_data = None
    return unload_ok


async def _async_options_updated(
    hass: HomeAssistant, entry: CoordinatorConfigEntry
) -> None:
    """Reload integration when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_entry(
    hass: HomeAssistant, entry: CoordinatorConfigEntry
) -> None:
    """Cleanup when an entry is fully removed by the user."""
    gateway_id = entry.data.get(GATEWAY_ID)
    Database.remove(gateway_id, delete_file=True)


async def start(coordinator: Coordinator):
    """Start the coordinator process."""
    try:
        coordinator.start()
    except VimarErrorResponseException as err:
        raise ConfigEntryAuthFailed(err) from err
    except CodeNotValidException as err:
        raise ConfigEntryAuthFailed(err) from err


# --- Restart service ------------------------------------------------------
# Registered once on first entry setup. Idempotent: the `has_service` guard
# means subsequent entries don't re-register. Persists for the lifetime of
# the HA process even if every entry is unloaded — minor cosmetic trade-off
# for simpler lifecycle. Issue #33: provides a manual escape hatch on top
# of the Coordinator watchdog.


def _async_register_restart_service(hass: HomeAssistant) -> None:
    if hass.services.has_service(DOMAIN, SERVICE_RESTART):
        return

    async def _handle_restart(call: ServiceCall) -> None:
        target_id = call.data.get(ATTR_ENTRY_ID)
        if target_id:
            entry = hass.config_entries.async_get_entry(target_id)
            if entry is None or entry.domain != DOMAIN:
                raise HomeAssistantError(
                    f"No vimar_byme_plus entry with id={target_id!r}"
                )
            entries = [entry]
        else:
            entries = list(hass.config_entries.async_entries(DOMAIN))
        for entry in entries:
            await hass.config_entries.async_reload(entry.entry_id)

    hass.services.async_register(
        DOMAIN, SERVICE_RESTART, _handle_restart, schema=RESTART_SERVICE_SCHEMA
    )
