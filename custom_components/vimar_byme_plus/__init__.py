"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

import logging
from functools import partial

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, GATEWAY_ID

_LOGGER = logging.getLogger(__name__)
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
    """Set up the integration from a config entry."""
    gateway_id = entry.data.get(GATEWAY_ID)
    if gateway_id:
        await hass.async_add_executor_job(Database.instance, gateway_id)
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


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate to v2: scope every entity's unique_id by gateway deviceuid.

    `base_entity.unique_id` now embeds the gateway uid
    (`vimar_byme_plus_<gw_uid>_app_<idsf>`) to avoid cross-gateway idsf
    collisions. Existing installs created before this change hold the legacy
    `vimar_byme_plus_app_<idsf>` ids; without this migration those entities
    would be orphaned (unavailable) and brand-new ones created at boot,
    losing every user customisation.

    Design is deliberately minimal: only `unique_id` is rewritten.
    entity_id, friendly name, area, device, icon — everything else is left
    untouched. The migration is idempotent (already-scoped ids are skipped)
    and defensive (a registry ValueError on one entity is logged and the
    loop continues; that entity simply keeps its legacy id).
    """
    if entry.version >= 2:
        return True

    gateway_uid = entry.data.get(GATEWAY_ID)
    if not gateway_uid:
        _LOGGER.warning(
            "Migration: entry %s has no gateway id, skipping unique_id rescoping",
            entry.entry_id,
        )
        hass.config_entries.async_update_entry(entry, version=2)
        return True

    legacy_prefix = f"{DOMAIN}_app_"
    new_prefix = f"{DOMAIN}_{gateway_uid}_app_"

    registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(registry, entry.entry_id)

    migrated = skipped = failed = 0
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

    hass.config_entries.async_update_entry(entry, version=2)
    return True


async def _async_options_updated(
    hass: HomeAssistant, entry: CoordinatorConfigEntry
) -> None:
    """Reload integration when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_entry(
    hass: HomeAssistant, entry: CoordinatorConfigEntry
) -> None:
    gateway_id = entry.data.get(GATEWAY_ID)
    if not gateway_id:
        return
    await hass.async_add_executor_job(partial(Database.remove, gateway_id, delete_file=True))


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
