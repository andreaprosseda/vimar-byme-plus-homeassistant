from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_button import VimarButton
from .....model.component.vimar_component import VimarComponent
from .....model.component.vimar_switch import VimarSwitch
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from ..base_action_handler import BaseActionHandler

ON_OFF = SfeType.CMD_ON_OFF
START_STOP = SfeType.CMD_IMMEDIATE_START_STOP
SKIP_ZONE = SfeType.CMD_SKIP_ZONE


class IrrigationActionHandler(BaseActionHandler):
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_auto_mode_actions(component)
        if action_type == ActionType.OFF:
            return self.get_turn_off_auto_mode_actions(component)
        if action_type == ActionType.PRESS:
            return self.get_press_actions(component)
        raise NotImplementedError

    def get_turn_on_auto_mode_actions(
        self, component: VimarSwitch
    ) -> list[VimarAction]:
        raise NotImplementedError
        # return [self._action(component.main_id, ON_OFF, "On")]

    def get_turn_off_auto_mode_actions(
        self, component: VimarSwitch
    ) -> list[VimarAction]:
        raise NotImplementedError
        # return [self._action(component.main_id, ON_OFF, "On")]

    def get_press_actions(self, component: VimarButton) -> list[VimarAction]:
        if "start_stop" in component.id:
            return self.get_start_stop_actions(component.main_id)
        if "skip" in component.id:
            return self.get_skip_zone_actions(component.main_id)
        raise NotImplementedError

    def get_start_stop_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, START_STOP, "Execute")]

    def get_skip_zone_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, SKIP_ZONE, "Execute")]
