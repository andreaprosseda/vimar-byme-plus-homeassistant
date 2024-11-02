from .ss_shutter_position_action_handler import SsShutterPositionActionHandler
from .ss_shutter_without_position_action_handler import SsShutterWithoutPositionActionHandler
from .....model.enum.action_type import ActionType
from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from ..base_action_handler import HandlerInterface

class ShutterActionHandler:
    
    def get_actions(self, component: VimarComponent, action_type: ActionType, *args) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)
    
    @staticmethod
    def get_handler(component: VimarComponent) -> HandlerInterface:
        sstype = component.device_name
        if sstype == SsShutterPositionActionHandler.SSTYPE:
            return SsShutterPositionActionHandler()
        if sstype == SsShutterWithoutPositionActionHandler.SSTYPE:
            return SsShutterWithoutPositionActionHandler()
        raise NotImplementedError
