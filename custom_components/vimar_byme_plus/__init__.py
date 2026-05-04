"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .coordinator import Coordinator
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException

_LOGGER = logging.getLogger(__name__)

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


async def async_setup_entry(hass: HomeAssistant, entry: CoordinatorConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    coordinator = Coordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
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
    entry.runtime_data = None
    return unload_ok


async def async_remove_config_entry_device(
    hass: HomeAssistant, entry: ConfigEntry, device_entry
) -> bool:
    """Allow removing a single device via the HA UI without removing the config entry.

    Returning True means: HA may detach this device from the config entry.
    The next coordinator refresh will re-create the device only if the
    Vimar gateway still publishes the corresponding idsf — so users can use
    this to prune stale ghost devices left over from plant reconfigurations.
    """
    return True


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entry to schema version 2.

    v1 -> v2: schema bump only. The integration now scopes device identifiers
    and entity unique_ids per gateway (see base_entity.py — issue #34), but
    we intentionally do **not** rewrite existing registry rows automatically
    here. An automatic in-place rename is fragile in real-world installs
    that may have user-renamed entity_ids, disabled-but-orphan rows, or
    leftovers from past plant reconfigurations — failure modes are tricky
    to recover from on the user side.

    Upgrade path for existing single-gateway installs:
      * On startup, the integration will publish entities with the new
        gateway-scoped unique_ids. Old non-scoped registry rows are left
        in place but become unavailable (no integration emits their uid
        anymore). Users can remove them from the UI at their convenience.
      * If preserving entity_ids / automation references matters, the
        cleanest path is: remove the config entry and re-pair. This
        recreates everything fresh under the new scheme.

    Multi-gateway installs that suffered from the pre-fix collision MUST
    re-pair (the registry contains genuinely ambiguous rows that no
    automatic migration can disambiguate).
    """
    if entry.version < 2:
        _LOGGER.info(
            "Bumping Vimar By-me Plus entry '%s' to schema v2 (gateway-scoped "
            "identifiers). Existing entities will be replaced with scoped "
            "versions on next coordinator refresh; orphan rows can be cleaned "
            "from the UI.",
            entry.title,
        )
        hass.config_entries.async_update_entry(entry, version=2)
    return True


async def start(coordinator: Coordinator):
    """Start the coordinator process."""
    try:
        coordinator.start()
    except VimarErrorResponseException as err:
        raise ConfigEntryAuthFailed(err) from err
    except CodeNotValidException as err:
        raise ConfigEntryAuthFailed(err) from err
