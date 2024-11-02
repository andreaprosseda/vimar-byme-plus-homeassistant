from .ss_light_dimmer_mapper import SsLightDimmerMapper
from .ss_light_switch_mapper import SsLightSwitchMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sftype_enum import SfType


class LightMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarLight]:
        sftype = SfType.LIGHT.value
        shutters = [component for component in components if component.sftype == sftype]
        return [LightMapper.from_obj(shutter) for shutter in shutters]

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarLight:
        mapper = LightMapper.get_mapper(component)
        return mapper.from_obj(component, *args)

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsLightSwitchMapper.SSTYPE:
            return SsLightSwitchMapper()
        if sstype == SsLightDimmerMapper.SSTYPE:
            return SsLightDimmerMapper()
        raise NotImplementedError
