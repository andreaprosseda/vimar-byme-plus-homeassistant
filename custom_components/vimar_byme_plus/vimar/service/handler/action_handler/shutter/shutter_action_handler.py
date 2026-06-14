from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_curtain_position_action_handler import SsCurtainPositionActionHandler
from .ss_curtain_without_position_action_handler import (
    SsCurtainWithoutPositionActionHandler,
)
from .ss_shutter_position_action_handler import SsShutterPositionActionHandler
from .ss_shutter_slat_position_action_handler import SsShutterSlatPositionActionHandler
from .ss_shutter_slat_without_position_action_handler import (
    SsShutterSlatWithoutPositionActionHandler,
)
from .ss_shutter_without_position_action_handler import (
    SsShutterWithoutPositionActionHandler,
)


class ShutterActionHandler:
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
        if sstype == SsShutterPositionActionHandler.SSTYPE:
            return SsShutterPositionActionHandler(gw)
        if sstype == SsShutterWithoutPositionActionHandler.SSTYPE:
            return SsShutterWithoutPositionActionHandler(gw)
        if sstype == SsShutterSlatPositionActionHandler.SSTYPE:
            return SsShutterSlatPositionActionHandler(gw)
        if sstype == SsShutterSlatWithoutPositionActionHandler.SSTYPE:
            return SsShutterSlatWithoutPositionActionHandler(gw)
        if sstype == SsCurtainPositionActionHandler.SSTYPE:
            return SsCurtainPositionActionHandler(gw)
        if sstype == SsCurtainWithoutPositionActionHandler.SSTYPE:
            return SsCurtainWithoutPositionActionHandler(gw)
        raise NotImplementedError
