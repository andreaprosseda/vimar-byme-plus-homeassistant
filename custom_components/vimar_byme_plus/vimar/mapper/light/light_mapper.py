from .ss_light_dimmer_mapper import SsLightDimmerMapper
from .ss_light_switch_mapper import SsLightSwitchMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sftype_enum import SfType
from ...utils.logger import not_implemented
from ...utils.filtering import flat


class LightMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarLight]:
        sftype = SfType.LIGHT.value
        lights = [component for component in components if component.sftype == sftype]
        components = [LightMapper.from_obj(light) for light in lights]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarLight]:
        try:
            mapper = LightMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsLightSwitchMapper.SSTYPE:
            return SsLightSwitchMapper()
        if sstype == SsLightDimmerMapper.SSTYPE:
            return SsLightDimmerMapper()
        raise NotImplementedError
