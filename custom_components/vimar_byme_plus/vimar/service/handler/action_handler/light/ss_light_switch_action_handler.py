from .....model.enum.action_type import ActionType
from .....model.enum.sftype_enum import SfType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from ..base_action_handler import BaseActionHandler

ON_OFF = SfeType.CMD_ON_OFF

class SsLightSwitchActionHandler(BaseActionHandler):
    SFTYPE = SfType.LIGHT.value
    SSTYPE = SsType.LIGHT_SWITCH.value


    def get_actions(self, component: VimarComponent, action_type: ActionType, *args) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component.id)
        if action_type == ActionType.OFF:
            return self.get_turn_off_actions(component.id)
        raise NotImplementedError
            
    def get_turn_on_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, ON_OFF, "On")]
    
    def get_turn_off_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, ON_OFF, "Off")]