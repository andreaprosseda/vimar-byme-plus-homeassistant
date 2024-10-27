from ....model.repository.user_component import UserComponent
from ....model.component.vimar_light import VimarLight, ColorMode
from ....model.enum.sftype_enum import SfType
from ....model.enum.sfetype_enum import SfeType
from ....model.enum.sstype_enum import SsType


class SsLightDimmerMapper:
    SFTYPE = SfType.LIGHT.value
    SSTYPE = SsType.LIGHT_DIMMER.value

    def from_obj(self, component: UserComponent, *args)-> VimarLight:
        return VimarLight(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sftype,
            area=component.ambient.name,
            is_on=self.get_is_on(component),
            brightness=self.get_brightness(component),
            color_mode=None,
            hs_color=None,
            xy_color=None,
            rgb_color=None,
            rgbw_color=None,
            rgbww_color=None,
            effect_list=None,
            effect=None,
            supported_color_modes=self.get_supported_color_modes(component),
        )

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "On" if value else False
    
    def get_brightness(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_BRIGHTNESS)
        if value.isdigit:
            return int(value)
        return None # Change up/Change down

    def get_supported_color_modes(self, component: UserComponent) -> set[ColorMode]:
        return { ColorMode.BRIGHTNESS }