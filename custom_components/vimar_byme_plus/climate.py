"""Platform for climate integration."""

from __future__ import annotations

import logging
from typing import Any

from xknx import XKNX

from homeassistant.components.climate import (
    PRESET_AWAY,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_NONE,
    PRESET_SLEEP,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, PRECISION_TENTHS, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import VimarDataUpdateCoordinator
from .vimar.climate.custom_climate import CustomClimate
from .vimar.climate.custom_climate_mode import CustomClimateMode
from .vimar.climate.custom_hvac_mode import (
    HVACControllerMode as CustomHVACControllerMode,
    HVACOperationMode as CustomHVACOperationMode,
)
from .vimar.model.byme_configuration.application import Application
from .vimar.model.vimar_addresses import VimarAddresses
from .vimar.model.vimar_application import VimarApplication, VimarType
from .vimar.vimar_entity import VimarEntity

HVAC_MODES = [HVACMode.HEAT, HVACMode.COOL]

HVAC_OPERATION_MODE_VALUES = {
    CustomHVACOperationMode.AUTO: PRESET_NONE,
    CustomHVACOperationMode.COMFORT: PRESET_COMFORT,
    CustomHVACOperationMode.STANDBY: PRESET_AWAY,
    CustomHVACOperationMode.NIGHT: PRESET_SLEEP,
    CustomHVACOperationMode.FROST_PROTECTION: PRESET_ECO,
    CustomHVACOperationMode.OFF: PRESET_NONE,
}

HVAC_MODE_VALUES = {
    CustomHVACControllerMode.COOL: HVACMode.COOL,
    CustomHVACControllerMode.HEAT: HVACMode.HEAT,
}

HVAC_ACTIONS = {
    HVACMode.HEAT: HVACAction.HEATING,
    HVACMode.COOL: HVACAction.COOLING,
    HVACMode.OFF: HVACAction.OFF,
    # HVACAction.IDLE,
}

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    hass_entry = hass.data[DOMAIN][entry.entry_id]
    coordinator: VimarDataUpdateCoordinator = hass_entry[DATA_COORDINATOR]
    apps = coordinator.config.get_entities(VimarType.CLIMA)
    entities = [VimarClimate(coordinator, app) for app in apps]
    _LOGGER.debug("Climates found: %s", len(entities))
    async_add_entities(entities, True)


class VimarClimate(VimarEntity, ClimateEntity):
    """Provides a Vimar climate."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    # _attr_fan_modes = [FAN_AUTO, FAN_ON, FAN_LOW, FAN_MEDIUM, FAN_HIGH]

    _device: CustomClimate

    _default_operation_mode = CustomHVACOperationMode.AUTO
    _default_controller_mode = CustomHVACControllerMode.HEAT
    _default_mode = HVACMode.HEAT
    _last_hvac_mode: HVACMode
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(
        self, coordinator: VimarDataUpdateCoordinator, app: VimarApplication
    ) -> None:
        """Initialize the climate."""
        device = self._register_knx_device(coordinator.knx, app)
        VimarEntity.__init__(self, coordinator, app, device)
        self._last_hvac_mode = self._default_mode

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Get supported features."""
        return (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.PRESET_MODE
            # | ClimateEntityFeature.FAN_MODE
        )

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        value = self._device.temperature.value
        _LOGGER.debug("[%s] Current Temperature: %s", self.name, value)
        return value

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        value = self._device.target_temperature.value
        _LOGGER.debug("[%s] Target Temperature: %s", self.name, value)
        return value

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        temp = self._device.target_temperature_min
        return temp if temp is not None else super().min_temp

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        temp = self._device.target_temperature_max
        return temp if temp is not None else super().max_temp

    @property
    def precision(self) -> float:
        """Get the precision based on the unit."""
        return PRECISION_TENTHS  # PRECISION_HALVES

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available operation/controller modes."""
        return HVAC_MODES

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current operation ie. heat, cool, idle."""
        mode = self._device.mode.controller_mode
        hvac_mode = HVAC_MODE_VALUES.get(mode, self._default_mode)
        if hvac_mode is not HVACMode.OFF:
            self._last_hvac_mode = hvac_mode
        return hvac_mode

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set controller mode."""
        if hvac_mode == HVACMode.OFF:
            await self.async_turn_off()
        else:
            controller_mode = self._get_controller_mode(hvac_mode)
            _LOGGER.debug(
                "[%s] Setting %s from %s", self.name, controller_mode, hvac_mode
            )
            await self._device.mode.set_controller_mode(controller_mode)
            self.async_write_ha_state()

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current running hvac operation if supported."""
        mode = self._device.mode
        _LOGGER.info("[%s] OperationMode %s", self.name, mode.operation_mode.value)
        _LOGGER.info("[%s] ControllerMode %s", self.name, mode.controller_mode.value)
        # NEED TO MANAGE IDLE
        hvac_mode = self.hvac_mode
        action = HVAC_ACTIONS.get(hvac_mode, HVACAction.IDLE)
        _LOGGER.info("[%s] Action %s from Mode %s", self.name, action, hvac_mode)
        return action

    @property
    def preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes."""
        return list(HVAC_OPERATION_MODE_VALUES.values())

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode, e.g., home, away, temp."""
        current_value = self._device.mode.operation_mode
        return HVAC_OPERATION_MODE_VALUES.get(current_value, PRESET_NONE)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        operation_mode = self._get_operation_mode(preset_mode)
        await self._device.mode.set_operation_mode(operation_mode)
        self.async_write_ha_state()

    # @property
    # def fan_modes(self) -> list[str]:
    #     """Return the list of available fan modes."""
    #     return self._fan_modes

    # @property
    # def fan_mode(self) -> str | None:
    #     """Return the fan setting."""
    #     return self._current_fan_mode

    # async def async_set_fan_mode(self, fan_mode: str) -> None:
    #     """Set new fan mode."""
    #     if (blower := self._blower) is not None:
    #         await blower.set_state(self._fan_mode_map[fan_mode])

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            await self._device.set_target_temperature(temperature)
            self.async_write_ha_state()

    async def async_toggle(self) -> None:
        """Toggle the entity."""
        if self.hvac_mode == HVACMode.OFF:
            await self.async_turn_on()
        else:
            await self.async_turn_off()

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        mode = self._last_hvac_mode
        controller_mode = self._get_controller_mode(mode)
        _LOGGER.info("Setting Controller Mode %s", controller_mode)
        await self._device.mode.set_controller_mode(controller_mode)
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        _LOGGER.info("Setting Controller Mode %s", "OFF")
        await self._device.mode.set_operation_mode(CustomHVACOperationMode.OFF)
        self.async_write_ha_state()

    def _get_operation_mode(self, preset_mode: str) -> CustomHVACOperationMode:
        for operation_mode, preset_mode_name in HVAC_OPERATION_MODE_VALUES.items():
            if preset_mode_name == preset_mode:
                return operation_mode
        return self._default_operation_mode

    def _get_controller_mode(self, hvac_mode: HVACMode) -> CustomHVACControllerMode:
        _LOGGER.info("Get Controller from: %s", hvac_mode)
        if hvac_mode == HVACMode.OFF:
            hvac_mode = self._last_hvac_mode
        for controller_mode, related_hvac_mode in HVAC_MODE_VALUES.items():
            if related_hvac_mode == hvac_mode:
                return controller_mode
        return self._default_controller_mode

    async def async_added_to_hass(self) -> None:
        """Store register state change callback."""
        await super().async_added_to_hass()
        self._device.mode.register_device_updated_cb(self.after_update_callback)

    def _register_knx_device(self, knx: XKNX, app: VimarApplication) -> CustomClimate:
        addresses = self._get_addresses(app.application)
        climate = self._get_climate(knx, app.application, addresses)
        knx.devices.add(climate)
        return climate

    def _get_climate(
        self, knx: XKNX, app: Application, addresses: VimarAddresses
    ) -> CustomClimate:
        return CustomClimate(
            xknx=knx,
            name=app.label,
            group_address_temperature=addresses.ambient_temperature,
            group_address_target_temperature=addresses.temperature_setpoint,
            group_address_target_temperature_state=addresses.temperature_setpoint_info,
            min_temp=16,
            max_temp=40,
            mode=self._get_climate_mode(knx, app, addresses),
        )

    def _get_climate_mode(
        self, knx: XKNX, app: Application, addresses: VimarAddresses
    ) -> CustomClimateMode:
        return CustomClimateMode(
            xknx=knx,
            name=app.label + "_mode",
            group_address_operation_mode=addresses.hvac_mode,
            group_address_operation_mode_state=addresses.hvac_mode_info,
            group_address_controller_mode=addresses.change_over_mode,
            group_address_controller_mode_state=addresses.change_over_mode_info,
            operation_modes=HVAC_OPERATION_MODE_VALUES.keys(),
            controller_modes=HVAC_MODE_VALUES.keys(),
        )
