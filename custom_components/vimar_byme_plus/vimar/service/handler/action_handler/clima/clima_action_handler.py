from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_climate import (
    FanMode,
    HVACMode,
    PresetMode,
    VimarClimate,
    ChangeOverMode,
)
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from ..base_action_handler import BaseActionHandler

HVAC_MODE = SfeType.CMD_HVAC_MODE
CHANGE_OVER_MODE = SfeType.CMD_CHANGE_OVER_MODE
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
        if mode == HVACMode.OFF.value:
            return self._set_previous_hvac_mode_off(component)
        if not component.can_change_mode:
            return self._set_previous_hvac_mode_on(component)
        return self._set_hvac_mode(component, mode)

    def set_preset_mode(self, id: str, mode: str) -> list[VimarAction]:
        preset_mode = PresetMode.get_preset_mode(mode)
        if not preset_mode:
            return []
        return [self._action(id, HVAC_MODE, preset_mode.vimar_value)]

    def set_temperature(self, component: VimarClimate, temp: str) -> list[VimarAction]:
        result = self._set_previous_hvac_mode_on(component)
        result.extend(self._get_timed_manual_if_needed(component))
        result.append(self._action(component.id, SETPOINT, temp))
        return result

    def set_fan_level(self, id: str, fan_mode: str) -> list[VimarAction]:
        change_mode = self._get_fan_mode(id, fan_mode)
        level = self._get_fan_level(id, fan_mode)
        return [change_mode, level] if level else [change_mode]

    def _set_hvac_mode(self, component: VimarClimate, mode: str) -> list[VimarAction]:
        value = component.on_behaviour.vimar_value
        hvac_mode = self._action(component.id, HVAC_MODE, value)
        change_over_mode = self._get_change_over_mode(component, mode)
        return [hvac_mode, change_over_mode] if change_over_mode else [hvac_mode]

    def _get_change_over_mode(self, component: VimarClimate, mode: str) -> VimarAction:
        heat = ChangeOverMode.HEAT.value
        cool = ChangeOverMode.COOL.value
        if mode == HVACMode.HEAT.value:
            return self._action(component.id, CHANGE_OVER_MODE, heat)
        if mode == HVACMode.COOL.value:
            return self._action(component.id, CHANGE_OVER_MODE, cool)
        return None

    def _set_previous_hvac_mode_off(self, component: VimarClimate) -> list[VimarAction]:
        value = component.off_behaviour.vimar_value
        return [self._action(component.id, HVAC_MODE, value)]

    def _set_previous_hvac_mode_on(self, component: VimarClimate) -> list[VimarAction]:
        value = component.on_behaviour.vimar_value
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

    def _get_timed_manual_if_needed(self, component: VimarClimate) -> list[VimarAction]:
        if component.on_behaviour == PresetMode.AUTO:
            return self.set_preset_mode(
                component.id, PresetMode.TIMED_MANUAL.vimar_value
            )
        return []
