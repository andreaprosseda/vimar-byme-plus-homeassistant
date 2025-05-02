from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler

SHUTTER = SfeType.CMD_SHUTTER_WITHOUT_POSITION


class SsShutterWithoutPositionActionHandler(BaseActionHandler):
    SSTYPE = SsType.SHUTTER_WITHOUT_POSITION.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.OPEN:
            return self.get_open_cover_actions(component.id)
        if action_type == ActionType.CLOSE:
            return self.get_close_cover_actions(component.id)
        if action_type == ActionType.STOP:
            return self.get_stop_cover_actions(component.id)
        raise NotImplementedError

    def get_open_cover_actions(self, id: str) -> list[VimarAction]:
        """Open the cover."""
        return [self._action(id, SHUTTER, "Up")]

    def get_close_cover_actions(self, id: str) -> list[VimarAction]:
        """Close cover."""
        return [self._action(id, SHUTTER, "Down")]

    def get_stop_cover_actions(self, id: str) -> list[VimarAction]:
        """Stop the cover."""
        return [self._action(id, SHUTTER, "Stop")]
