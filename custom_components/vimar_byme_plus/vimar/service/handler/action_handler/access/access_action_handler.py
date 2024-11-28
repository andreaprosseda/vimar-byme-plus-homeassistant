from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from ..base_action_handler import BaseActionHandler

ON_OFF = SfeType.CMD_ON_OFF


class AccessActionHandler(BaseActionHandler):
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.OPEN:
            return self.get_open_cover_actions(component.id)
        if action_type == ActionType.SET_LEVEL:
            return self.get_open_cover_actions(component.id, args[0])
        raise NotImplementedError

    def set_cover_position(self, id: str, position: str) -> list[VimarAction]:
        if position and int(position) > 0:
            return [self._action(id, ON_OFF, "On")]
        return []

    def get_open_cover_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, ON_OFF, "On")]
