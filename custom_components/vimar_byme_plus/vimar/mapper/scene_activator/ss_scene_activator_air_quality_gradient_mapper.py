from ...model.component.vimar_button import VimarButton
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneActivatorAirQualityGradientMapper:
    SSTYPE = SsType.SCENE_ACTIVATOR_AIR_QUALITY_GRADIENT.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarButton:
        raise NotImplementedError
