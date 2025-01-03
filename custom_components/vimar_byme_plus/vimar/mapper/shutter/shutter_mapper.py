from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_curtain_position_mapper import SsCurtainPositionMapper
from .ss_curtain_without_position_mapper import SsCurtainWithoutPositionMapper
from .ss_shutter_position_mapper import SsShutterPositionMapper
from .ss_shutter_slat_position_mapper import SsShutterSlatPositionMapper
from .ss_shutter_slat_without_position_mapper import SsShutterSlatWithoutPositionMapper
from .ss_shutter_without_position_mapper import SsShutterWithoutPositionMapper


class ShutterMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.SHUTTER.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [ShutterMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = ShutterMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(__name__, component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsShutterPositionMapper.SSTYPE:
            return SsShutterPositionMapper()
        if sstype == SsShutterWithoutPositionMapper.SSTYPE:
            return SsShutterWithoutPositionMapper()
        if sstype == SsShutterSlatPositionMapper.SSTYPE:
            return SsShutterSlatPositionMapper()
        if sstype == SsShutterSlatWithoutPositionMapper.SSTYPE:
            return SsShutterSlatWithoutPositionMapper()
        if sstype == SsCurtainPositionMapper.SSTYPE:
            return SsCurtainPositionMapper()
        if sstype == SsCurtainWithoutPositionMapper.SSTYPE:
            return SsCurtainWithoutPositionMapper()
        raise NotImplementedError
