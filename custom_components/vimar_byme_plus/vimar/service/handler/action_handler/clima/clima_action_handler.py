from .....model.enum.action_type import ActionType
from .....model.component.vimar_climate import (
    VimarClimate,
    PresetMode,
    HVACMode,
    FanMode,
)
from .....model.component.vimar_component import VimarComponent
from .....model.component.vimar_action import VimarAction
from ..base_action_handler import BaseActionHandler
from .....model.enum.sfetype_enum import SfeType

HVAC_MODE = SfeType.CMD_HVAC_MODE
SETPOINT = SfeType.CMD_AMBIENT_SETPOINT
FAN_MODE = SfeType.CMD_FAN_MODE
FAN = SfeType.CMD_FAN_SPEED_3V
ON_STATE = SfeType.STATE_ON_BEHAVIOUR
OFF_STATE = SfeType.STATE_OFF_BEHAVIOUR


class ClimaActionHandler(BaseActionHandler):
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.SET_HVAC_MODE:
            return self.set_hvac_mode(component, args[0])
        if action_type == ActionType.SET_PRESET_MODE:
            return self.set_preset_mode(component.id, args[0])
        if action_type == ActionType.SET_TEMP:
            return self.set_temperature(component, args[0])
        if action_type == ActionType.SET_LEVEL:
            return self.set_fan_level(component.id, args[0])
        raise NotImplementedError

    def set_hvac_mode(self, component: VimarClimate, mode: str) -> list[VimarAction]:
        if mode == HVACMode.OFF.ha_value:
            return self._get_previous_hvac_mode_off(component)
        return self._get_previous_hvac_mode_on(component)

    def set_preset_mode(self, id: str, mode: str) -> list[VimarAction]:
        preset_mode = PresetMode.get_preset_mode(mode)
        if not preset_mode:
            return []
        return [self._action(id, HVAC_MODE, preset_mode.vimar_value)]

    def set_temperature(self, component: VimarClimate, temp: str) -> list[VimarAction]:
        result = self._get_previous_hvac_mode_on_if_needed(component)
        result.extend(self._get_timed_manual_if_needed(component))
        result.append(self._action(component.id, SETPOINT, temp))
        return result

    def set_fan_level(self, id: str, fan_mode: str) -> list[VimarAction]:
        change_mode = self._get_fan_mode(id, fan_mode)
        level = self._get_fan_level(id, fan_mode)
        return [change_mode, level] if level else [change_mode]

    def _get_previous_hvac_mode_on(self, component: VimarClimate) -> list[VimarAction]:
        value = component.on_behaviour.vimar_value
        return [self._action(component.id, HVAC_MODE, value)]

    def _get_previous_hvac_mode_off(self, component: VimarClimate) -> list[VimarAction]:
        value = component.off_behaviour.vimar_value
        return [self._action(component.id, HVAC_MODE, value)]

    def _get_fan_mode(self, id: str, fan_mode: str) -> VimarAction:
        if fan_mode == FanMode.AUTOMATIC.ha_value:
            return self._action(id, FAN_MODE, "Automatic")
        return self._action(id, FAN_MODE, "Manual")

    def _get_fan_level(self, id: str, fan_mode: str) -> VimarAction:
        if fan_mode == FanMode.FAN_LOW.ha_value:
            return self._action(id, FAN, FanMode.FAN_LOW.vimar_value)
        if fan_mode == FanMode.FAN_MEDIUM.ha_value:
            return self._action(id, FAN, FanMode.FAN_MEDIUM.vimar_value)
        if fan_mode == FanMode.FAN_HIGH.ha_value:
            return self._action(id, FAN, FanMode.FAN_HIGH.vimar_value)
        return None

    def _get_previous_hvac_mode_on_if_needed(
        self, component: VimarClimate
    ) -> list[VimarAction]:
        if component.hvac_mode == HVACMode.OFF:
            return self.set_hvac_mode(component, HVACMode.AUTO.vimar_value)
        return []

    def _get_timed_manual_if_needed(self, component: VimarClimate) -> list[VimarAction]:
        if component.on_behaviour == PresetMode.AUTO:
            return self.set_preset_mode(
                component.id, PresetMode.TIMED_MANUAL.vimar_value
            )
        return []
