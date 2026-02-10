from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_button import VimarButton
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_scene_activator_activator_action_handler import (
    SsSceneActivatorActivatorActionHandler,
)

EXECUTE_DESCENDING = SfeType.CMD_AIR_QUALITY_GRADIENT_DESCENDING_ACTIVE_SCENE
EXECUTE_STABILIZATION = SfeType.CMD_AIR_QUALITY_GRADIENT_STABILIZATION_ACTIVE_SCENE

class SsSceneActivatorAirQualityGradientActionHandler(SsSceneActivatorActivatorActionHandler):
    SSTYPE = SsType.SCENE_ACTIVATOR_AIR_QUALITY_GRADIENT.value

    def get_press_actions(self, component: VimarButton) -> list[VimarAction]:
        if "descending" in component.id:
            return self.get_press_descending_actions(component.id)
        if "stabilization" in component.id:
            return self.get_press_stabilization_actions(component.id)
        raise NotImplementedError

    def get_press_descending_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, EXECUTE_DESCENDING, "Execute")]
    
    def get_press_stabilization_actions(self, id: str) -> list[VimarAction]:
        return [self._action(id, EXECUTE_STABILIZATION, "Execute")]
