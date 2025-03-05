from ...model.component.vimar_binary_sensor import VimarBinarySensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSensorLuminosityMapper:
    SSTYPE = SsType.SENSOR_LUMINOSITY.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarBinarySensor]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarBinarySensor:
        raise NotImplementedError
