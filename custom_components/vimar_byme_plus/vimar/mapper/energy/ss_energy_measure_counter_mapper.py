from decimal import ROUND_HALF_UP, Decimal

from ...model.component.vimar_sensor import (
    SensorDeviceClass,
    SensorMeasurementUnit,
    VimarSensor,
)
from ...model.enum.sstype_enum import SsType
from ...model.enum.sfetype_enum import SfeType
from ...model.repository.user_component import UserComponent
from ..base_mapper import BaseMapper


class SsEnergyMeasureCounterMapper(BaseMapper):
    SSTYPE = SsType.ENERGY_MEASURE_COUNTER.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=str(component.idsf),
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ENERGY,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=None,
            unit_of_measurement=SensorMeasurementUnit.KILO_WATT_HOUR,
            state_class=None,
            options=None,
        )

    def native_value(self, component: UserComponent) -> Decimal | None:
        value = component.get_value(SfeType.STATE_PARTIAL_COUNTER)
        if not value:
            return None
        decimal_value = Decimal(value) / 1000
        return decimal_value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
