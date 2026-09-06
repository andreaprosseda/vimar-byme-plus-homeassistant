from decimal import Decimal

from ...model.component.vimar_sensor import (
    SensorDeviceClass,
    SensorMeasurementUnit,
    SensorStateClass,
    VimarSensor,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_sensor_generic_mapper import SsSensorGenericMapper


class SsSensorTemperatureMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_TEMPERATURE.value
    SFETYPE = SfeType.STATE_SENSOR_TEMPERATURE
    NAME_SUFFIX = ""
    STATE_CLASS = None

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf if not args else args[0],
            name=self.name(component),
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.TEMPERATURE,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.CELSIUS,
            state_class=self.STATE_CLASS,
            options=None,
        )

    def _button_real_time(self, component: UserComponent, *args):
        return None  # Optional by Vimar

    def name(self, component: UserComponent) -> str:
        if not self.NAME_SUFFIX:
            return component.name
        return component.name + " - " + self.NAME_SUFFIX

    def native_value(self, component: UserComponent) -> str | Decimal | None:
        value = component.get_value(self.SFETYPE)
        if value:
            return Decimal(value)
        return None

    def decimal_precision(self, component: UserComponent) -> int:
        return 1


class SsSensorTemperatureMinMapper(SsSensorTemperatureMapper):
    """Lowest temperature of the current day, reset by the station at midnight."""

    SFETYPE = SfeType.STATE_SENSOR_TEMPERATURE_MIN
    NAME_SUFFIX = "Temperature Min"
    STATE_CLASS = SensorStateClass.MEASUREMENT


class SsSensorTemperatureMaxMapper(SsSensorTemperatureMapper):
    """Highest temperature of the current day, reset by the station at midnight."""

    SFETYPE = SfeType.STATE_SENSOR_TEMPERATURE_MAX
    NAME_SUFFIX = "Temperature Max"
    STATE_CLASS = SensorStateClass.MEASUREMENT


class SsSensorAbsoluteTemperatureMinMapper(SsSensorTemperatureMapper):
    """Lowest temperature ever recorded by the station."""

    SFETYPE = SfeType.STATE_ABSOLUTE_SENSOR_TEMPERATURE_MIN
    NAME_SUFFIX = "Temperature Min All Time"


class SsSensorAbsoluteTemperatureMaxMapper(SsSensorTemperatureMapper):
    """Highest temperature ever recorded by the station."""

    SFETYPE = SfeType.STATE_ABSOLUTE_SENSOR_TEMPERATURE_MAX
    NAME_SUFFIX = "Temperature Max All Time"
