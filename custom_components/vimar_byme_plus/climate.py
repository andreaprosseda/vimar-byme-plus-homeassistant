"""Platform for cover integration."""

from __future__ import annotations

from functools import reduce
from typing import Any

from homeassistant.components.climate import (
    ATTR_TEMPERATURE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_climate import VimarClimate
from .vimar.model.enum.action_type import ActionType
from .vimar.utils.logger import log_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_climates()
    entities = [Climate(coordinator, component) for component in components]
    log_info(__name__, f"Climates found: {len(entities)}")
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
        """Return the unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT)."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_humidity(self) -> float | None:
        """Return the current humidity."""
        return self._component.current_humidity

    @property
    def target_humidity(self) -> float | None:
        """Return the target humidity the device is trying to reach."""
        return self._component.target_humidity

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return the current operation (e.g. heat, cool, idle). Used to determine state."""
        mode = self._component.hvac_mode
        return HVACMode(mode.value) if mode else None

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available hvac operation modes."""
        modes = self._component.hvac_modes
        return [HVACMode(mode.value) for mode in modes] if modes else []

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current running hvac operation if supported. The current HVAC action (heating, cooling)."""
        action = self._component.hvac_action
        return HVACAction(action.value) if action else None

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self._component.current_temperature

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature currently set to be reached."""
        return self._component.target_temperature

    @property
    def target_temperature_step(self) -> float | None:
        """Return the supported step of target temperature. Can be increased or decreased."""
        return self._component.target_temperature_step

    @property
    def target_temperature_high(self) -> float | None:
        """Return the highbound target temperature we try to reach. Requires ClimateEntityFeature.TARGET_TEMPERATURE_RANGE."""
        return self._component.target_temperature_high

    @property
    def target_temperature_low(self) -> float | None:
        """Return the lowbound target temperature we try to reach. Requires ClimateEntityFeature.TARGET_TEMPERATURE_RANGE."""
        return self._component.target_temperature_low

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode, e.g., home, away, temp. Requires ClimateEntityFeature.PRESET_MODE."""
        return self._component.preset_mode

    @property
    def preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes. Requires ClimateEntityFeature.PRESET_MODE."""
        return self._component.preset_modes

    @property
    def fan_mode(self) -> str | None:
        """Return the fan setting. Requires ClimateEntityFeature.FAN_MODE."""
        mode = self._component.fan_mode
        return mode.ha_value if mode else None

    @property
    def fan_modes(self) -> list[str] | None:
        """Return the list of available fan modes. Requires ClimateEntityFeature.FAN_MODE."""
        return [mode.ha_value for mode in self._component.fan_modes]

    @property
    def swing_mode(self) -> str | None:
        """Return the swing setting. Requires ClimateEntityFeature.SWING_MODE."""
        return self._component.swing_mode

    @property
    def swing_modes(self) -> list[str] | None:
        """Return the list of available swing modes. Requires ClimateEntityFeature.SWING_MODE."""
        return self._component.swing_modes

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return the list of supported features defined by using values in the ClimateEntityFeature enum and are combined using the bitwise or (|) operator."""
        features = [f.value for f in self._component.supported_features]
        return reduce(lambda x, y: x | y, features, ClimateEntityFeature(0))

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature in temperature_unit."""
        return self._component.min_temp

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature in temperature_unit."""
        return self._component.max_temp

    @property
    def min_humidity(self) -> float:
        """Return the minimum humidity."""
        return self._component.min_humidity

    @property
    def max_humidity(self) -> float:
        """Return the maximum humidity."""
        return self._component.max_humidity

    def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if not self._component.permission_granted:
            message = "Insufficient permissions to set HVAC mode. Please refer to the ‘Grant Right Permissions’ section in GitHub README."
            raise HomeAssistantError(message)
        self.send(ActionType.SET_HVAC_MODE, hvac_mode.value)

    def set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        self.send(ActionType.SET_TEMP, temperature)

    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        self.send(ActionType.SET_LEVEL, fan_mode)

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        self.send(ActionType.SET_PRESET_MODE, preset_mode)
