from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_automation_on_off_action_handler import SsAutomationOnOffActionHandler
from .ss_automation_output_control_action_handler import (
    SsAutomationOutputControlActionHandler,
)


class AutomationActionHandler:
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
        if sstype == SsAutomationOnOffActionHandler.SSTYPE:
            return SsAutomationOnOffActionHandler(gw)
        if sstype == SsAutomationOutputControlActionHandler.SSTYPE:
            return SsAutomationOutputControlActionHandler(gw)
        raise NotImplementedError
