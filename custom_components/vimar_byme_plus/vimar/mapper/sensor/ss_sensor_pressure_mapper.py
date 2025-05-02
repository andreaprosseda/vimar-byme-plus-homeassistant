from decimal import Decimal

from ...model.component.vimar_sensor import (
    SensorDeviceClass,
    SensorMeasurementUnit,
    VimarSensor,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_sensor_generic_mapper import SsSensorGenericMapper


class SsSensorPressureMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_PRESSURE.value

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.PRESSURE,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.PASCAL,
            state_class=None,
            options=None,
        )

    def native_value(self, component: UserComponent) -> str | Decimal | None:
        value = component.get_value(SfeType.STATE_PRESSURE)
        if value:
            return Decimal(value)
        return None

    def decimal_precision(self, component: UserComponent) -> int:
        return 0
