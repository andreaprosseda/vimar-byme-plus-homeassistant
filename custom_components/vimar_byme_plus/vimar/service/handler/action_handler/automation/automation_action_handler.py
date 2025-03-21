from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_automation_on_off_action_handler import SsAutomationOnOffActionHandler
from .ss_automation_output_control_action_handler import (
    SsAutomationOutputControlActionHandler,
)


class AutomationActionHandler:
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)

    @staticmethod
    def get_handler(component: VimarComponent) -> HandlerInterface:
        sstype = component.device_name
        if sstype == SsAutomationOnOffActionHandler.SSTYPE:
            return SsAutomationOnOffActionHandler()
        if sstype == SsAutomationOutputControlActionHandler.SSTYPE:
            return SsAutomationOutputControlActionHandler()
        raise NotImplementedError
