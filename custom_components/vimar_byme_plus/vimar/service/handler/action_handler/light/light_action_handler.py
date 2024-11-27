from .ss_light_switch_action_handler import SsLightSwitchActionHandler
from .ss_light_dimmer_action_handler import SsLightDimmerActionHandler
from .....model.enum.action_type import ActionType
from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from ..base_action_handler import HandlerInterface


class LightActionHandler:
    
    def get_actions(self, component: VimarComponent, action_type: ActionType, *args) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)

    @staticmethod
    def get_handler(component: VimarComponent) -> HandlerInterface:
        sstype = component.device_name
        if sstype == SsLightSwitchActionHandler.SSTYPE:
            return SsLightSwitchActionHandler()
        if sstype == SsLightDimmerActionHandler.SSTYPE:
            return SsLightDimmerActionHandler()
        raise NotImplementedError
