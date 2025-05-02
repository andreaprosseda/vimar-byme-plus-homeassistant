from ...model.component.vimar_light import ColorMode
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_light_switch_mapper import SsLightSwitchMapper


class SsLightDimmerMapper(SsLightSwitchMapper):
    SSTYPE = SsType.LIGHT_DIMMER.value

    def get_brightness(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_BRIGHTNESS)
        if value and value.isdigit():
            return int(value)
        return None  # Change up/Change down

    def get_color_mode(self, component: UserComponent) -> ColorMode:
        return ColorMode.BRIGHTNESS

    def get_supported_color_modes(self, component: UserComponent) -> set[ColorMode]:
        return {ColorMode.BRIGHTNESS}
