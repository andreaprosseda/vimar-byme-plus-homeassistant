from .....model.enum.action_type import ActionType
from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from ..base_action_handler import BaseActionHandler

class ClimaActionHandler(BaseActionHandler):
    
    def get_actions(self, component: VimarComponent, action_type: ActionType, *args) -> list[VimarAction]:
        raise NotImplementedError