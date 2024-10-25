from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType

SFTYPE = SfType.LIGHT.value


class LightMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarLight]:
        return [LightMapper.from_obj(c) for c in components if c.sftype == SFTYPE]

    @staticmethod
    def from_obj(component: UserComponent) -> VimarLight:
        return VimarLight(
            id=component.idsf,
            name=component.name,
            device_name=component.sftype,
            area=component.ambient.name,
            is_on=LightMapper.get_is_on(component),
            brightness=None,
            color_mode=None,
            hs_color=None,
            xy_color=None,
            rgb_color=None,
            rgbw_color=None,
            rgbww_color=None,
            effect_list=None,
            effect=None,
            supported_color_modes=None,
        )

    def get_is_on(component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "On" if value else False
