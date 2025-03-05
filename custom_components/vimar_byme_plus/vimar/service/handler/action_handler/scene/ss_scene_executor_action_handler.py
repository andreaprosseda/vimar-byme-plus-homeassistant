from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler

EXECUTE = SfeType.CMD_EXECUTE


class SsSceneExecutorActionHandler(BaseActionHandler):
    SSTYPE = SsType.SCENE_EXECUTOR.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.PRESS:
            return self.get_press_actions(component.id)
        raise NotImplementedError

    def get_press_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, EXECUTE, "Execute")]
