"""VIMAR By-me Plus HUB integration."""

from __future__ import annotations

from functools import partial

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN, GATEWAY_ID
from .coordinator import Coordinator
from .vimar.database.database import Database
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException
from .vimar.utils.logger import log_info, log_warning

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
RESTART_SERVICE_SCHEMA = vol.Schema({vol.Optional(ATTR_ENTRY_ID): str})


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
    """Migrate identifiers to the per-gateway scoped format."""
    gateway_uid = entry.data.get(GATEWAY_ID)
    if not gateway_uid:
        log_warning(
            __name__, f"Entry {entry.entry_id} has no gateway id, skipping rescoping"
        )
        if entry.version < 3:
            hass.config_entries.async_update_entry(entry, version=3)
        return True

    if entry.version < 2:
        _rescope_entity_unique_ids(hass, entry, gateway_uid)
        hass.config_entries.async_update_entry(entry, version=2)

    if entry.version < 3:
        _rescope_device_identifiers(hass, entry, gateway_uid)
        hass.config_entries.async_update_entry(entry, version=3)

    return True


def _rescope_entity_unique_ids(
    hass: HomeAssistant, entry: ConfigEntry, gateway_uid: str
) -> None:
    """v1 -> v2: rewrite `vimar_byme_plus_app_<idsf>` unique_ids to the
    gateway-scoped `vimar_byme_plus_<deviceuid>_app_<idsf>` form."""
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
        new_uid = new_prefix + uid[len(legacy_prefix) :]
        try:
            registry.async_update_entity(ent.entity_id, new_unique_id=new_uid)
            migrated += 1
        except ValueError as err:
            log_warning(
                __name__,
                f"Migration: cannot rescope entity {ent.entity_id} ({uid} -> {new_uid}): {err}",
            )
            failed += 1

    log_info(
        __name__,
        f"Migration entry {entry.entry_id} (gateway {gateway_uid}): entities rescoped {migrated}, already-ok {skipped}, failed {failed}",
    )


def _rescope_device_identifiers(
    hass: HomeAssistant, entry: ConfigEntry, gateway_uid: str
) -> None:
    """Rewrite (DOMAIN, <component_id>) device identifier to the gateway-scoped (DOMAIN, "<deviceuid>_<component_id>") form."""
    registry = dr.async_get(hass)
    devices = dr.async_entries_for_config_entry(registry, entry.entry_id)
    new_prefix = f"{gateway_uid}_"

    migrated = skipped = failed = 0
    for device in devices:
        new_identifiers = set()
        changed = False
        for domain, ident in device.identifiers:
            ident_str = str(ident)
            if domain != DOMAIN or ident_str.startswith(new_prefix):
                new_identifiers.add((domain, ident))
                continue
            new_identifiers.add((domain, f"{new_prefix}{ident_str}"))
            changed = True
        if not changed:
            skipped += 1
            continue
        try:
            registry.async_update_device(device.id, new_identifiers=new_identifiers)
            migrated += 1
        except (ValueError, KeyError) as err:
            log_warning(
                __name__, f"Migration: cannot rescope device {device.id}: {err}"
            )
            failed += 1
    log_info(
        __name__,
        f"Migration entry {entry.entry_id} (gateway {gateway_uid}): devices rescoped {migrated}, already-ok {skipped}, failed {failed}",
    )


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
    await hass.async_add_executor_job(
        partial(Database.remove, gateway_id, delete_file=True)
    )


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
