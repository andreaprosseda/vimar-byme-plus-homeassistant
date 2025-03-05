from .ss_scene_activator_activator_mapper import SsSceneActivatorActivatorMapper
from .ss_scene_activator_air_quality_gradient_mapper import (
    SsSceneActivatorAirQualityGradientMapper,
)
from .ss_scene_activator_sai_mapper import SsSceneActivatorSaiMapper
from .ss_scene_activator_sai_g2_mapper import SsSceneActivatorSaiG2Mapper
from .ss_scene_activator_video_entry_mapper import SsSceneActivatorVideoEntryMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...utils.logger import not_implemented
from ...utils.filtering import flat


class SceneActivatorMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.SCENE.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [SceneActivatorMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = SceneActivatorMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(__name__, component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsSceneActivatorActivatorMapper.SSTYPE:
            return SsSceneActivatorActivatorMapper()
        if sstype == SsSceneActivatorAirQualityGradientMapper.SSTYPE:
            return SsSceneActivatorAirQualityGradientMapper()
        if sstype == SsSceneActivatorSaiMapper.SSTYPE:
            return SsSceneActivatorSaiMapper()
        if sstype == SsSceneActivatorSaiG2Mapper.SSTYPE:
            return SsSceneActivatorSaiG2Mapper()
        if sstype == SsSceneActivatorVideoEntryMapper.SSTYPE:
            return SsSceneActivatorVideoEntryMapper()
        raise NotImplementedError
