from .ss_light_dimmer_action_handler import SsLightDimmerActionHandler
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.component.vimar_light import VimarLight

ON_OFF = SfeType.CMD_ON_OFF
BRIGHTNESS = SfeType.CMD_BRIGHTNESS
RGB = SfeType.CMD_RGB
HSV = SfeType.CMD_HSV


class SsLightDimmerRgbActionHandler(SsLightDimmerActionHandler):
    SSTYPE = SsType.LIGHT_DIMMER_RGB.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component, args[0], args[1])
        return super().get_actions(component, action_type, *args)

    def get_turn_on_actions(
        self, component: VimarComponent, brightness: int, rgb: str
    ) -> list[VimarAction]:
        values = [self._action(component.id, ON_OFF, "On")]
        if brightness is not None:
            values.extend(self._get_hsv(component, brightness))
        if rgb:
            values.append(self._action(component.id, RGB, rgb))
        return values

    def _get_hsv(self, component: VimarLight, brightness: int) -> list[VimarAction]:
        hsv = component.hsv_color
        new_hsv = (hsv[0], hsv[1], brightness)
        value = ",".join(map(str, new_hsv))
        return [self._action(component.id, HSV, value)]
