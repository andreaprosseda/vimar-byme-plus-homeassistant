from ...model.component.vimar_light import ColorMode
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_light_philips_dynamic_dimmer_mapper import SsLightPhilipsDynamicDimmerMapper


class SsLightPhilipsDynamicDimmerRgbMapper(SsLightPhilipsDynamicDimmerMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_DYNAMIC_DIMMER_RGB.value

    def get_color_mode(self, component: UserComponent) -> ColorMode:
        return ColorMode.RGB

    def get_supported_color_modes(self, component: UserComponent) -> set[ColorMode]:
        return {ColorMode.COLOR_TEMP, ColorMode.RGB}

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
