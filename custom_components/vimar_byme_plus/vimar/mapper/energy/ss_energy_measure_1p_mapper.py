from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

from ...model.component.vimar_sensor import (
    SensorDeviceClass,
    SensorMeasurementUnit,
    SensorStateClass,
    VimarSensor,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ..base_mapper import BaseMapper


class SsEnergyMeasure1pMapper(BaseMapper):
    SSTYPE = SsType.ENERGY_MEASURE_1P.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [
            self.power_from_obj(component, *args),
            self.energy_from_obj(component, *args),
        ]

    def power_from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=str(component.idsf) + "_power",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.POWER,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=self.last_update(component),
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILO_WATT,
            state_class=SensorStateClass.MEASUREMENT,
            options=None,
        )

    def energy_from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=str(component.idsf) + "_energy",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ENERGY,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=self.last_update(component),
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            options=None,
        )

    def native_value(self, component: UserComponent) -> Decimal | None:
        value = component.get_value(SfeType.STATE_GLOBAL_ACTIVE_POWER_CONSUMPTION)
        if not value:
            return None
        decimal_value = Decimal(value) / 1000
        return decimal_value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

    def last_update(self, component: UserComponent) -> datetime | None:
        value = component.get_last_update(SfeType.STATE_GLOBAL_ACTIVE_POWER_CONSUMPTION)
        if not value:
            return None
        return datetime.fromisoformat(value)

    def decimal_precision(self, component: UserComponent) -> int:
        return 3
