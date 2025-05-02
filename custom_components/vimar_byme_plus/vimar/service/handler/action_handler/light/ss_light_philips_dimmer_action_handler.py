from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_light_dimmer_action_handler import SsLightDimmerActionHandler

ON_OFF = SfeType.CMD_ON_OFF
BRIGHTNESS = SfeType.CMD_BRIGHTNESS


class SsLightPhilipsDimmerActionHandler(SsLightDimmerActionHandler):
    SSTYPE = SsType.LIGHT_PHILIPS_DIMMER.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        return super().get_actions(component, action_type, *args)
