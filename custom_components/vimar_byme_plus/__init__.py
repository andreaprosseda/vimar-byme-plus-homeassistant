"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN, GATEWAY_ID
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


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entry to v2: scope every entity's unique_id by gateway_uid.

    Strategy chosen deliberately MINIMAL after two earlier attempts (v2.54
    and v2.56 in the project changelog) that broke user-renamed entity_ids:

    * Only `unique_id` is touched here. `entity_id`, friendly name, area,
      device_id, icon, anything else the user may have customised is left
      exactly as-is.
    * Idempotent: an entity whose `unique_id` already starts with
      `vimar_byme_plus_<gw_uid>_` is skipped.
    * Defensive: a `ValueError` from the registry (collision because some
      previous attempt left a partially scoped duplicate behind) is logged
      and the loop keeps going. Worst case for that entity: it stays on
      the legacy unscoped `unique_id` and the user can clean it up by
      deleting it from the UI; nothing else breaks.

    Why we need it: `base_entity.unique_id` now includes the gateway uid,
    so freshly-created entities at boot get
    `vimar_byme_plus_<gw_uid>_app_<idsf>`. Without this migration, the
    pre-existing entities would keep their legacy `vimar_byme_plus_app_<idsf>`
    and become orphan unavailable instances after the next start.
    """
    if entry.version >= 3:
        return True

    gateway_uid = entry.data.get(GATEWAY_ID)
    if not gateway_uid:
        _LOGGER.warning(
            "Migration: entry %s has no GATEWAY_ID, skipping unique_id rescoping",
            entry.entry_id,
        )
        hass.config_entries.async_update_entry(entry, version=3)
        return True

    legacy_prefix = f"{DOMAIN}_app_"
    new_prefix = f"{DOMAIN}_{gateway_uid}_app_"

    registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(registry, entry.entry_id)

    migrated = 0
    skipped = 0
    failed = 0
    for ent in entities:
        uid = ent.unique_id
        if not uid.startswith(legacy_prefix):
            skipped += 1
            continue
        new_uid = new_prefix + uid[len(legacy_prefix):]
        try:
            registry.async_update_entity(ent.entity_id, new_unique_id=new_uid)
            migrated += 1
        except ValueError as err:
            _LOGGER.warning(
                "Migration: cannot rescope %s (%s -> %s): %s",
                ent.entity_id, uid, new_uid, err,
            )
            failed += 1

    _LOGGER.info(
        "Migration entry %s (gateway %s): rescoped %d, already-ok %d, failed %d",
        entry.entry_id, gateway_uid, migrated, skipped, failed,
    )

    hass.config_entries.async_update_entry(entry, version=3)
    return True


async def start(coordinator: Coordinator):
    """Start the coordinator process."""
    try:
        coordinator.start()
    except VimarErrorResponseException as err:
        raise ConfigEntryAuthFailed(err) from err
    except CodeNotValidException as err:
        raise ConfigEntryAuthFailed(err) from err
