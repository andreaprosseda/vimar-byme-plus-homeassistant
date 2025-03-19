from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_scene_activator_activator_action_handler import (
    SsSceneActivatorActivatorActionHandler,
)
from .ss_scene_activator_video_entry_action_handler import (
    SsSceneActivatorVideoEntryActionHandler,
)


class SceneActivatorActionHandler:
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)

    @staticmethod
    def get_handler(component: VimarComponent) -> HandlerInterface:
        sstype = component.device_name
        if sstype == SsSceneActivatorActivatorActionHandler.SSTYPE:
            return SsSceneActivatorActivatorActionHandler()
        if sstype == SsSceneActivatorVideoEntryActionHandler.SSTYPE:
            return SsSceneActivatorVideoEntryActionHandler()
        raise NotImplementedError
