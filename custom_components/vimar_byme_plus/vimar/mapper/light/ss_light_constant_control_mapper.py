from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sstype_enum import SsType


class SsLightConstantControlMapper:
    SSTYPE = SsType.LIGHT_CONSTANT_CONTROL.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarLight]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarLight:
        raise NotImplementedError
