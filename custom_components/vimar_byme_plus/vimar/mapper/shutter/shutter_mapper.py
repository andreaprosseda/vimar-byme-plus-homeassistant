from .ss_curtain_position_mapper import SsCurtainPositionMapper
from .ss_curtain_without_position_mapper import SsCurtainWithoutPositionMapper
from .ss_shutter_position_mapper import SsShutterPositionMapper
from .ss_shutter_without_position_mapper import SsShutterWithoutPositionMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_cover import VimarCover
from ...model.enum.sftype_enum import SfType
from ...utils.logger import not_implemented
from ...utils.filtering import filter_none


class ShutterMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarCover]:
        sftype = SfType.SHUTTER.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [ShutterMapper.from_obj(shutter) for shutter in shutters]
        return filter_none(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarCover:
        try:
            mapper = ShutterMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return None

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsShutterPositionMapper.SSTYPE:
            return SsShutterPositionMapper()
        if sstype == SsShutterWithoutPositionMapper.SSTYPE:
            return SsShutterWithoutPositionMapper()
        if sstype == SsCurtainPositionMapper.SSTYPE:
            return SsCurtainPositionMapper()
        if sstype == SsCurtainWithoutPositionMapper.SSTYPE:
            return SsCurtainWithoutPositionMapper()
        raise NotImplementedError
