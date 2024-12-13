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
        if action_type == ActionType.CLOSE:
            return self.get_close_cover_actions(component.id)
        if action_type == ActionType.SET_POSITION:
            return self.get_set_cover_position(component.id, args[0])
        raise NotImplementedError

    def get_set_cover_position(self, id: str, position: str) -> list[VimarAction]:
        if position:
            return [self._action(id, ON_OFF, "On")]
        return []

    def get_open_cover_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, ON_OFF, "On")]

    def get_close_cover_actions(self, id: str) -> list[VimarAction]:
        return []
