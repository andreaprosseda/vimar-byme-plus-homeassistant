from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_button import VimarButton
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler

EXECUTE = SfeType.CMD_TIMED_DYNAMIC_MODE


class SsSensorPowerActionHandler(BaseActionHandler):
    SSTYPE = SsType.SENSOR_POWER.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.PRESS:
            return self.get_press_actions(component)
        raise NotImplementedError

    def get_press_actions(self, component: VimarButton) -> list[VimarAction]:
        return [self._action(component.id, EXECUTE, "Start")]
