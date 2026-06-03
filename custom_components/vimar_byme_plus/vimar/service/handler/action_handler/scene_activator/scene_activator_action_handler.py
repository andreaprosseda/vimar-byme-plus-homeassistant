from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_scene_activator_activator_action_handler import (
    SsSceneActivatorActivatorActionHandler,
)
from .ss_scene_activator_air_quality_gradient_action_handler import (
    SsSceneActivatorAirQualityGradientActionHandler,
)
from .ss_scene_activator_sai_action_handler import SsSceneActivatorSaiActionHandler
from .ss_scene_activator_sai_g2_action_handler import (
    SsSceneActivatorSaiG2ActionHandler,
)
from .ss_scene_activator_video_entry_action_handler import (
    SsSceneActivatorVideoEntryActionHandler,
)


class SceneActivatorActionHandler:
    
    def __init__(self, gateway_id: str) -> None:
        self._gateway_id = gateway_id

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)

    def get_handler(self, component: VimarComponent) -> HandlerInterface:
        gw = self._gateway_id
        sstype = component.device_name
        if sstype == SsSceneActivatorActivatorActionHandler.SSTYPE:
            return SsSceneActivatorActivatorActionHandler(gw)
        if sstype == SsSceneActivatorAirQualityGradientActionHandler.SSTYPE:
            return SsSceneActivatorAirQualityGradientActionHandler(gw)
        if sstype == SsSceneActivatorSaiActionHandler.SSTYPE:
            return SsSceneActivatorSaiActionHandler(gw)
        if sstype == SsSceneActivatorSaiG2ActionHandler.SSTYPE:
            return SsSceneActivatorSaiG2ActionHandler(gw)
        if sstype == SsSceneActivatorVideoEntryActionHandler.SSTYPE:
            return SsSceneActivatorVideoEntryActionHandler(gw)
        raise NotImplementedError
