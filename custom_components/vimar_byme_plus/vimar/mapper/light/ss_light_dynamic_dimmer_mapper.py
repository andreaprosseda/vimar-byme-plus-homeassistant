from ...model.component.vimar_light import ColorMode
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_light_dimmer_mapper import SsLightDimmerMapper


class SsLightDynamicDimmerMapper(SsLightDimmerMapper):
    SSTYPE = SsType.LIGHT_DYNAMIC_DIMMER.value

    def get_color_mode(self, component: UserComponent) -> ColorMode:
        return ColorMode.COLOR_TEMP

    def get_supported_color_modes(self, component: UserComponent) -> set[ColorMode]:
        return {ColorMode.COLOR_TEMP}

    def get_temp_color(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_MIXING_WHITE_VALUE)
        if value and value.isdigit():
            return int(value)
        return None  # Change up/Change down
