from .....model.enum.action_type import ActionType
from .....model.component.vimar_climate import HVACAction, HVACMode, ChangeOverMode
from .....model.component.vimar_component import VimarComponent
from .....model.component.vimar_action import VimarAction
from ..base_action_handler import BaseActionHandler
from .....model.enum.sfetype_enum import SfeType

ON_OFF = SfeType.CMD_ON_OFF
SETPOINT = SfeType.STATE_AMBIENT_SETPOINT
# HVAC_MODE = SfeType.CMD_HVAC_MODE
HVAC_MODE = SfeType.STATE_CHANGE_OVER_MODE
FAN = SfeType.CMD_FAN_SPEED_3V


class ClimaActionHandler(BaseActionHandler):
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component.id)
        if action_type == ActionType.OFF:
            return self.get_turn_off_actions(component.id)
        if action_type == ActionType.SET_HVAC_MODE:
            return self.get_set_hvac_mode(component.id, args[0])
        if action_type == ActionType.SET_TEMP:
            return self.get_set_temperature(component.id, args[0])
        if action_type == ActionType.SET_LEVEL:
            return self.get_set_fan_level(component.id, args[0])
        raise NotImplementedError

    def get_turn_on_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, HVAC_MODE, "Manual")]

    def get_turn_off_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, HVAC_MODE, "Off")]

    def get_set_hvac_mode(self, id: str, hvac_mode: str) -> list[VimarAction]:
        if hvac_mode == HVACMode.COOL.ha_value:
            return [self._action(id, HVAC_MODE, ChangeOverMode.COOL.value)]
        if hvac_mode == HVACMode.HEAT.ha_value:
            return [self._action(id, HVAC_MODE, ChangeOverMode.HEAT.value)]
        if hvac_mode == HVACMode.OFF.ha_value:
            return self.get_turn_off_actions(id)
        raise NotImplementedError

    def get_set_temperature(self, id: str, temperature: str) -> list[VimarAction]:
        return [self._action(id, SETPOINT, temperature)]

    def get_set_fan_level(self, id: str, fan_mode: str) -> list[VimarAction]:
        return [self._action(id, FAN, fan_mode)]
