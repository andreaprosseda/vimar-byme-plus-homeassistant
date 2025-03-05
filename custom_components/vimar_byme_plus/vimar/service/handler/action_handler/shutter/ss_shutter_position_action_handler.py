from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler

SHUTTER = SfeType.CMD_SHUTTER


class SsShutterPositionActionHandler(BaseActionHandler):
    SSTYPE = SsType.SHUTTER_POSITION.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.OPEN:
            return self.get_open_cover_actions(component.id)
        if action_type == ActionType.CLOSE:
            return self.get_close_cover_actions(component.id)
        if action_type == ActionType.STOP:
            return self.get_stop_cover_actions(component.id)
        if action_type == ActionType.SET_POSITION:
            return self.get_set_cover_position_actions(component.id, args[0])
        raise NotImplementedError

    def get_open_cover_actions(self, id: str) -> list[VimarAction]:
        """Open the cover."""
        return [self._action(id, SHUTTER, "0")]

    def get_close_cover_actions(self, id: str) -> list[VimarAction]:
        """Close cover."""
        return [self._action(id, SHUTTER, "100")]

    def get_stop_cover_actions(self, id: str) -> list[VimarAction]:
        """Stop the cover."""
        return [self._action(id, SHUTTER, "Stop")]

    def get_set_cover_position_actions(
        self, id: str, position: int
    ) -> list[VimarAction]:
        """Move the cover to a specific position."""
        return [self._action(id, SHUTTER, str(position))]
