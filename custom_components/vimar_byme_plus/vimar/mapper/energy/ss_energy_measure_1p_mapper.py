from decimal import Decimal, ROUND_HALF_UP
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_sensor import (
    VimarSensor,
    SensorDeviceClass,
    SensorStateClass,
    SensorMeasurementUnit,
)
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType


class SsEnergyMeasure1pMapper(BaseMapper):
    SFTYPE = SfType.ENERGY.value
    SSTYPE = SsType.ENERGY_MEASURE_1P.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [self._from_obj(component, *args)]
    
    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.POWER,
            area=component.ambient.name,
            native_value=self.native_value(component),
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILO_WATT,
            state_class=SensorStateClass.MEASUREMENT,
            options=None,
        )

    def native_value(self, component: UserComponent) -> Decimal | None:
        value = component.get_value(SfeType.STATE_GLOBAL_ACTIVE_POWER_CONSUMPTION)
        if not value:
            return None
        decimal_value = Decimal(value) / 1000
        return decimal_value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

    def decimal_precision(self, component: UserComponent) -> int:
        return 3
