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


class SsSensorWindSpeedMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_WIND_SPEED.value

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf if not args else args[0],
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.WIND_SPEED,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.get_kmh(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILOMETERS_PER_HOUR,
            state_class=None,
            options=None,
        )

    def get_kmh(self, component: UserComponent) -> Decimal | None:
        value = self.native_value(component)
        if not value:
            return None
        return value * Decimal("3.6")

    def native_value(self, component: UserComponent) -> Decimal | None:
        value = component.get_value(SfeType.STATE_WIND_SPEED)
        if value:
            return Decimal(value)
        return None

    def decimal_precision(self, component: UserComponent) -> int:
        return 1
