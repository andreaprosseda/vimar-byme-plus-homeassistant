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
        if sstype == SsLightSwitchActionHandler.SSTYPE:
            return SsLightSwitchActionHandler(gw)
        if sstype == SsLightDimmerActionHandler.SSTYPE:
            return SsLightDimmerActionHandler(gw)
        if sstype == SsLightDimmerRgbActionHandler.SSTYPE:
            return SsLightDimmerRgbActionHandler(gw)
        if sstype == SsLightDynamicDimmerActionHandler.SSTYPE:
            return SsLightDynamicDimmerActionHandler(gw)
        if sstype == SsLightPhilipsDimmerActionHandler.SSTYPE:
            return SsLightPhilipsDimmerActionHandler(gw)
        if sstype == SsLightPhilipsDimmerRgbActionHandler.SSTYPE:
            return SsLightPhilipsDimmerRgbActionHandler(gw)
        if sstype == SsLightPhilipsSwitchActionHandler.SSTYPE:
            return SsLightPhilipsSwitchActionHandler(gw)
        if sstype == SsLightPhilipsDynamicDimmerActionHandler.SSTYPE:
            return SsLightPhilipsDynamicDimmerActionHandler(gw)
        if sstype == SsLightPhilipsDynamicDimmerRgbActionHandler.SSTYPE:
            return SsLightPhilipsDynamicDimmerRgbActionHandler(gw)
        raise NotImplementedError
