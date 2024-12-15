from .ss_irrigation_multi_zones_mapper import SsIrrigationMultiZonesMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...utils.logger import not_implemented
from ...utils.filtering import flat


class IrrigationMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.IRRIGATION.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [IrrigationMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = IrrigationMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsIrrigationMultiZonesMapper.SSTYPE:
            return SsIrrigationMultiZonesMapper()
        raise NotImplementedError
