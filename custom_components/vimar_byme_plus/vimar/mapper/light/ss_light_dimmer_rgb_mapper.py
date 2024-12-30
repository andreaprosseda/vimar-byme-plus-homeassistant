from .ss_light_dimmer_mapper import SsLightDimmerMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import ColorMode
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType


class SsLightDimmerRgbMapper(SsLightDimmerMapper):
    SSTYPE = SsType.LIGHT_DIMMER_RGB.value

    def get_brightness(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_HSV)
        if value and "," in value:
            return int(value.split(",")[2])
        return None

    def get_hsv_color(self, component: UserComponent) -> tuple[int, int, int] | None:
        value = component.get_value(SfeType.STATE_HSV)
        if value and "," in value:
            return tuple(map(int, value.split(",")))
        return None  # Changing

    def get_rgb_color(self, component: UserComponent) -> tuple[int, int, int] | None:
        value = component.get_value(SfeType.STATE_RGB)
        if value and "," in value:
            return tuple(map(int, value.split(",")))
        return None  # Changing

    def get_supported_color_modes(self, component: UserComponent) -> set[ColorMode]:
        return {ColorMode.BRIGHTNESS, ColorMode.RGB}
