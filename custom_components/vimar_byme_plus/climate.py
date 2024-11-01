"""Platform for cover integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base_entity import BaseEntity
from . import CoordinatorConfigEntry
from .coordinator import Coordinator
from .vimar.model.component.vimar_climate import VimarClimate
from .vimar.utils.logger import log_debug


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_climates()
    entities = [Climate(coordinator, component) for component in components]
    log_debug(__name__, f"Climates found: {len(entities)}")
    async_add_entities(entities, True)


class Climate(BaseEntity, ClimateEntity):
    """Provides a Vimar Cover."""

    _component: VimarClimate
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, coordinator: Coordinator, component: VimarClimate) -> None:
        """Initialize the clima."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement used by the platform.

        HomeAssistant Description: The unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT).
        """
        return UnitOfTemperature.CELSIUS

    @property
    def current_humidity(self) -> float | None:
        """Return the current humidity.

        HomeAssistant Description: The current humidity.
        """
        return self._component.current_humidity

    @property
    def target_humidity(self) -> float | None:
        """Return the humidity we try to reach.

        HomeAssistant Description: The target humidity the device is trying to reach.
        """
        return self._component.target_humidity

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return hvac operation ie. heat, cool mode.

        HomeAssistant Description: The current operation (e.g. heat, cool, idle). Used to determine state.
        """
        mode = self._component.hvac_mode
        if not mode:
            return None
        return HVACMode(mode.ha_value)

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available hvac operation modes.

        HomeAssistant Description: List of available operation modes. See below.
        """
        modes = self._component.hvac_modes
        if not modes:
            return []
        return [HVACMode(mode.ha_value) for mode in modes]

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current running hvac operation if supported.

        HomeAssistant Description: The current HVAC action (heating, cooling)
        """
        action = self._component.hvac_action
        if not action:
            return None
        return HVACAction(action.ha_value)

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature.

        HomeAssistant Description: The current temperature.
        """
        return self._component.current_temperature

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach.

        HomeAssistant Description: The temperature currently set to be reached.
        """
        return self._component.target_temperature

    @property
    def target_temperature_step(self) -> float | None:
        """Return the supported step of target temperature.

        HomeAssistant Description: The supported step size a target temperature can be increased or decreased
        """
        return self._component.target_temperature_step

    @property
    def target_temperature_high(self) -> float | None:
        """Return the highbound target temperature we try to reach.

        Requires ClimateEntityFeature.TARGET_TEMPERATURE_RANGE.

        HomeAssistant Description: The upper bound target temperature
        """
        return self._component.target_temperature_high

    @property
    def target_temperature_low(self) -> float | None:
        """Return the lowbound target temperature we try to reach.

        Requires ClimateEntityFeature.TARGET_TEMPERATURE_RANGE.

        HomeAssistant Description: The lower bound target temperature
        """
        return self._component.target_temperature_low

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode, e.g., home, away, temp.

        Requires ClimateEntityFeature.PRESET_MODE.

        HomeAssistant Description: The current active preset.
        """
        return self._component.preset_mode

    @property
    def preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes.

        Requires ClimateEntityFeature.PRESET_MODE.

        HomeAssistant Description: The available presets.
        """
        return self._component.preset_modes

    @property
    def fan_mode(self) -> str | None:
        """Return the fan setting.

        Requires ClimateEntityFeature.FAN_MODE.

        HomeAssistant Description: The current fan mode.
        """
        return self._component.fan_mode

    @property
    def fan_modes(self) -> list[str] | None:
        """Return the list of available fan modes.

        Requires ClimateEntityFeature.FAN_MODE.

        HomeAssistant Description: The list of available fan modes.
        """
        return self._component.fan_modes

    @property
    def swing_mode(self) -> str | None:
        """Return the swing setting.

        Requires ClimateEntityFeature.SWING_MODE.

        HomeAssistant Description: The swing setting.
        """
        return self._component.swing_mode

    @property
    def swing_modes(self) -> list[str] | None:
        """Return the list of available swing modes.

        Requires ClimateEntityFeature.SWING_MODE.

        HomeAssistant Description: Returns the list of available swing modes.
        """
        return self._component.swing_modes

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return the list of supported features.

        HomeAssistant Description: Supported features are defined by using values in the ClimateEntityFeature enum and are combined using the bitwise or (|) operator.
        """
        return (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.PRESET_MODE
        )

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature.

        HomeAssistant Description: The minimum temperature in temperature_unit.
        """
        return self._component.min_temp

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature.

        HomeAssistant Description: The maximum temperature in temperature_unit.
        """
        return self._component.max_temp

    @property
    def min_humidity(self) -> float:
        """Return the minimum humidity.

        HomeAssistant Description: The minimum humidity.
        """
        return self._component.min_humidity

    @property
    def max_humidity(self) -> float:
        """Return the maximum humidity.

        HomeAssistant Description: The maximum humidity.
        """
        return self._component.max_humidity

    def toggle(self) -> None:
        """Toggle the entity."""
        raise NotImplementedError

    def turn_off(self) -> None:
        """Turn the entity off."""
        raise NotImplementedError

    def turn_on(self) -> None:
        """Turn the entity on."""
        raise NotImplementedError

    def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        raise NotImplementedError

    def set_swing_mode(self, swing_mode: str) -> None:
        """Set new target swing operation."""
        raise NotImplementedError

    def set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        raise NotImplementedError

    def set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        raise NotImplementedError

    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        raise NotImplementedError
