from ....model.repository.user_component import UserComponent
from ....model.component.vimar_cover import VimarCover
from ..base_mapper import BaseMapper
from ....model.enum.sftype_enum import SfType
from .ss_shutter_position_mapper import SsShutterPositionMapper
from .ss_shutter_without_position_mapper import SsShutterWithoutPositionMapper


class ShutterMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarCover]:
        sftype = SfType.SHUTTER.value
        shutters = [component for component in components if component.sftype == sftype]
        return [ShutterMapper.from_obj(shutter) for shutter in shutters]

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarCover:
        mapper = ShutterMapper.get_mapper(component)
        return mapper.from_obj(component, *args)

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsShutterPositionMapper.SSTYPE:
            return SsShutterPositionMapper()
        if sstype == SsShutterWithoutPositionMapper.SSTYPE:
            return SsShutterWithoutPositionMapper()
        return NotImplementedError()
