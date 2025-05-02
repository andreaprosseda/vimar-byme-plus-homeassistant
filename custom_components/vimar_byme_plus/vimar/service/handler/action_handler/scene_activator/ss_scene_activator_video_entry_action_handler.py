from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_button import VimarButton
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_scene_activator_activator_action_handler import (
    SsSceneActivatorActivatorActionHandler,
)

START = SfeType.CMD_START_ACTIVE_SCENE
END = SfeType.CMD_END_ACTIVE_SCENE


class SsSceneActivatorVideoEntryActionHandler(SsSceneActivatorActivatorActionHandler):
    SSTYPE = SsType.SCENE_ACTIVATOR_VIDEO_ENTRY.value

    def get_press_actions(self, component: VimarButton) -> list[VimarAction]:
        if "start_call" in component.id:
            return self.get_start_call_actions(component.main_id)
        if "end_call" in component.id:
            return self.get_end_call_actions(component.main_id)
        raise NotImplementedError

    def get_start_call_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, START, "Execute")]

    def get_end_call_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, END, "Execute")]
