from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_light_dimmer_action_handler import SsLightDimmerActionHandler
from .ss_light_dimmer_rgb_action_handler import SsLightDimmerRgbActionHandler
from .ss_light_dynamic_dimmer_action_handler import SsLightDynamicDimmerActionHandler
from .ss_light_philips_dimmer_action_handler import SsLightPhilipsDimmerActionHandler
from .ss_light_philips_dimmer_rgb_action_handler import (
    SsLightPhilipsDimmerRgbActionHandler,
)
from .ss_light_philips_dynamic_dimmer_action_handler import (
    SsLightPhilipsDynamicDimmerActionHandler,
)
from .ss_light_philips_dynamic_dimmer_rgb_action_handler import (
    SsLightPhilipsDynamicDimmerRgbActionHandler,
)
from .ss_light_philips_switch_action_handler import SsLightPhilipsSwitchActionHandler
from .ss_light_switch_action_handler import SsLightSwitchActionHandler


class LightActionHandler:
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)

    @staticmethod
    def get_handler(component: VimarComponent) -> HandlerInterface:
        sstype = component.device_name
        if sstype == SsLightSwitchActionHandler.SSTYPE:
            return SsLightSwitchActionHandler()
        if sstype == SsLightDimmerActionHandler.SSTYPE:
            return SsLightDimmerActionHandler()
        if sstype == SsLightDimmerRgbActionHandler.SSTYPE:
            return SsLightDimmerRgbActionHandler()
        if sstype == SsLightDynamicDimmerActionHandler.SSTYPE:
            return SsLightDynamicDimmerActionHandler()
        if sstype == SsLightPhilipsDimmerActionHandler.SSTYPE:
            return SsLightPhilipsDimmerActionHandler()
        if sstype == SsLightPhilipsDimmerRgbActionHandler.SSTYPE:
            return SsLightPhilipsDimmerRgbActionHandler()
        if sstype == SsLightPhilipsSwitchActionHandler.SSTYPE:
            return SsLightPhilipsSwitchActionHandler()
        if sstype == SsLightPhilipsDynamicDimmerActionHandler.SSTYPE:
            return SsLightPhilipsDynamicDimmerActionHandler()
        if sstype == SsLightPhilipsDynamicDimmerRgbActionHandler.SSTYPE:
            return SsLightPhilipsDynamicDimmerRgbActionHandler()
        raise NotImplementedError
