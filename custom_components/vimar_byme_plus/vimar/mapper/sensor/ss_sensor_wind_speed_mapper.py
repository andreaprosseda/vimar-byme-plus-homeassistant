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


class SsSensorWindSpeedMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_WIND_SPEED.value
    SFETYPE = SfeType.STATE_WIND_SPEED
    NAME_SUFFIX = ""
    STATE_CLASS = None

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf if not args else args[0],
            name=self.name(component),
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.WIND_SPEED,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.get_kmh(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILOMETERS_PER_HOUR,
            state_class=self.STATE_CLASS,
            options=None,
        )

    def get_kmh(self, component: UserComponent) -> Decimal | None:
        value = self.native_value(component)
        if not value:
            return None
        return value * Decimal("3.6")

    def name(self, component: UserComponent) -> str:
        if not self.NAME_SUFFIX:
            return component.name
        return component.name + " - " + self.NAME_SUFFIX

    def native_value(self, component: UserComponent) -> Decimal | None:
        value = component.get_value(self.SFETYPE)
        if value:
            return Decimal(value)
        return None

    def decimal_precision(self, component: UserComponent) -> int:
        return 1


class SsSensorWindSpeedMaxMapper(SsSensorWindSpeedMapper):
    """Highest gust of the current day, reset by the station at midnight."""

    SFETYPE = SfeType.STATE_WIND_SPEED_MAX
    NAME_SUFFIX = "Wind Gust"
    STATE_CLASS = SensorStateClass.MEASUREMENT

    def _button_real_time(self, component: UserComponent, *args):
        # The real time button is keyed on the component id and is already
        # provided by the wind speed sensor of the same component.
        return None


class SsSensorAbsoluteWindSpeedMaxMapper(SsSensorWindSpeedMapper):
    """Highest gust ever recorded by the station."""

    SFETYPE = SfeType.STATE_ABSOLUTE_WIND_SPEED_MAX
    NAME_SUFFIX = "Wind Gust All Time"

    def _button_real_time(self, component: UserComponent, *args):
        return None
