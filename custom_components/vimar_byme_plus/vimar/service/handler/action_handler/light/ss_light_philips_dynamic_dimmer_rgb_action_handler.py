from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_light_philips_dynamic_dimmer_action_handler import (
    SsLightPhilipsDynamicDimmerActionHandler,
)

ON_OFF = SfeType.CMD_ON_OFF
BRIGHTNESS = SfeType.CMD_BRIGHTNESS
RGB = SfeType.CMD_RGB
WHITE = SfeType.CMD_MIXING_WHITE_VALUE


class SsLightPhilipsDynamicDimmerRgbActionHandler(
    SsLightPhilipsDynamicDimmerActionHandler
):
    SSTYPE = SsType.LIGHT_PHILIPS_DYNAMIC_DIMMER_RGB.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component, args[0], args[1], args[2])
        return super().get_actions(component, action_type, *args)

    def get_turn_on_actions(
        self, component: VimarComponent, brightness: int, rgb: str, white: int
    ) -> list[VimarAction]:
        values = [self._action(component.id, ON_OFF, "On")]
        values.extend(self._get_brightness(component.id, brightness))
        values.extend(self._get_rgb(component.id, rgb))
        values.extend(self._get_mixing_white_value(component.id, white))
        return values

    def _get_brightness(self, id: str, brightness: int) -> list[VimarAction]:
        if brightness is not None:
            return [self._action(id, BRIGHTNESS, brightness)]
        return []

    def _get_rgb(self, id: str, rgb: str) -> list[VimarAction]:
        if rgb:
            return [self._action(id, RGB, rgb)]
        return []

    def _get_mixing_white_value(self, id: str, white: int) -> list[VimarAction]:
        if white is not None:
            return [self._action(id, WHITE, white)]
        return []
