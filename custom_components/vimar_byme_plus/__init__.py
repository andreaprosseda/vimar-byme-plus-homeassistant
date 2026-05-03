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
    """Migrate config entry from previous schema versions.

    v1 -> v2: scope device identifiers and entity unique_ids per gateway,
    so that multi-gateway setups (issue #34) no longer collide on shared idsf.
    """
    _LOGGER.info(
        "Migrating Vimar By-me Plus entry %s from version %s",
        entry.title,
        entry.version,
    )

    if entry.version < 2:
        gateway_uid = entry.data.get(GATEWAY_ID) or entry.unique_id
        if not gateway_uid:
            _LOGGER.error(
                "Cannot migrate entry %s: no gateway uid available", entry.entry_id
            )
            return False

        device_reg = dr.async_get(hass)
        entity_reg = er.async_get(hass)

        # 1) Migrate device identifiers: (DOMAIN, idsf) -> (DOMAIN, f"{gw}_{idsf}")
        migrated_devices = 0
        for device in dr.async_entries_for_config_entry(device_reg, entry.entry_id):
            new_identifiers: set[tuple[str, str]] = set()
            changed = False
            for ident in device.identifiers:
                if ident[0] != DOMAIN:
                    new_identifiers.add(ident)
                    continue
                value = ident[1]
                value_str = str(value)
                # Already migrated by a previous attempt — leave as-is
                if isinstance(value, str) and value.startswith(f"{gateway_uid}_"):
                    new_identifiers.add(ident)
                    continue
                new_identifiers.add((DOMAIN, f"{gateway_uid}_{value_str}"))
                changed = True
            if changed:
                device_reg.async_update_device(
                    device.id, new_identifiers=new_identifiers
                )
                migrated_devices += 1

        # 2) Migrate entity unique_ids: vimar_byme_plus_app_<idsf>
        #    -> vimar_byme_plus_<gw>_app_<idsf>
        old_prefix = f"{DOMAIN}_app_"
        new_prefix = f"{DOMAIN}_{gateway_uid}_app_"
        migrated_entities = 0
        for entity in er.async_entries_for_config_entry(entity_reg, entry.entry_id):
            uid = entity.unique_id or ""
            if not uid.startswith(old_prefix):
                continue
            idsf = uid[len(old_prefix):]
            new_uid = f"{new_prefix}{idsf}"
            try:
                entity_reg.async_update_entity(entity.entity_id, new_unique_id=new_uid)
                migrated_entities += 1
            except ValueError:
                # collision: another entity already has the new unique_id
                # (rare — only happens if a previous failed migration left
                # both versions). Keep old, will be cleaned up by user.
                _LOGGER.warning(
                    "Could not migrate entity %s to %s (collision)",
                    entity.entity_id,
                    new_uid,
                )

        hass.config_entries.async_update_entry(entry, version=2)
        _LOGGER.info(
            "Migration complete for %s: %s devices, %s entities updated",
            entry.title,
            migrated_devices,
            migrated_entities,
        )

    return True


async def start(coordinator: Coordinator):
    """Start the coordinator process."""
    try:
        coordinator.start()
    except VimarErrorResponseException as err:
        raise ConfigEntryAuthFailed(err) from err
    except CodeNotValidException as err:
        raise ConfigEntryAuthFailed(err) from err
