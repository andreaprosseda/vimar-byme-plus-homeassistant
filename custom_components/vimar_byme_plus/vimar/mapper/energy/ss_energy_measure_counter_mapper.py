from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_sensor import (
    VimarSensor,
)
from ...model.enum.sstype_enum import SsType


class SsEnergyMeasureCounterMapper(BaseMapper):
    SSTYPE = SsType.ENERGY_MEASURE_COUNTER.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        raise NotImplementedError
