from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_light_constant_control_mapper import SsLightConstantControlMapper
from .ss_light_dimmer_mapper import SsLightDimmerMapper
from .ss_light_dimmer_rgb_mapper import SsLightDimmerRgbMapper
from .ss_light_dynamic_dimmer_mapper import SsLightDynamicDimmerMapper
from .ss_light_philips_dimmer_mapper import SsLightPhilipsDimmerMapper
from .ss_light_philips_dimmer_rgb_mapper import SsLightPhilipsDimmerRgbMapper
from .ss_light_philips_dynamic_dimmer_mapper import SsLightPhilipsDynamicDimmerMapper
from .ss_light_philips_dynamic_dimmer_rgb_mapper import (
    SsLightPhilipsDynamicDimmerRgbMapper,
)
from .ss_light_philips_switch_mapper import SsLightPhilipsSwitchMapper
from .ss_light_switch_mapper import SsLightSwitchMapper


class LightMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.LIGHT.value
        lights = [component for component in components if component.sftype == sftype]
        components = [LightMapper.from_obj(light) for light in lights]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = LightMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(__name__, component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsLightConstantControlMapper.SSTYPE:
            return SsLightConstantControlMapper()
        if sstype == SsLightDimmerMapper.SSTYPE:
            return SsLightDimmerMapper()
        if sstype == SsLightDimmerRgbMapper.SSTYPE:
            return SsLightDimmerRgbMapper()
        if sstype == SsLightDynamicDimmerMapper.SSTYPE:
            return SsLightDynamicDimmerMapper()
        if sstype == SsLightPhilipsDimmerMapper.SSTYPE:
            return SsLightPhilipsDimmerMapper()
        if sstype == SsLightPhilipsDimmerRgbMapper.SSTYPE:
            return SsLightPhilipsDimmerRgbMapper()
        if sstype == SsLightPhilipsDynamicDimmerMapper.SSTYPE:
            return SsLightPhilipsDynamicDimmerMapper()
        if sstype == SsLightPhilipsDynamicDimmerRgbMapper.SSTYPE:
            return SsLightPhilipsDynamicDimmerRgbMapper()
        if sstype == SsLightPhilipsSwitchMapper.SSTYPE:
            return SsLightPhilipsSwitchMapper()
        if sstype == SsLightSwitchMapper.SSTYPE:
            return SsLightSwitchMapper()
        raise NotImplementedError
