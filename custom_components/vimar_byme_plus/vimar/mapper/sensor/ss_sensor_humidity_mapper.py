from decimal import Decimal

from ...model.component.vimar_component import VimarComponent
from ...model.component.vimar_sensor import (
    SensorDeviceClass,
    SensorMeasurementUnit,
    VimarSensor,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_sensor_generic_mapper import SsSensorGenericMapper


class SsSensorHumidityMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_HUMIDITY.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarComponent]:
        """The ambient reading, plus the configured threshold when there is one.

        Per the Vimar spec a humidity component is a humidistat, not just a
        probe: besides SFE_State_Humidity it carries SFE_State_HumiditySetpoint
        (issue #95). The gateway was already storing the setpoint - it simply
        had no entity, so a threshold changed in the Vimar app was invisible
        to Home Assistant.
        """
        values = super().from_obj(component, *args)
        setpoint = self._setpoint_from_obj(component)
        if setpoint:
            values.append(setpoint)
        return values

    def _setpoint_from_obj(self, component: UserComponent) -> VimarSensor | None:
        """Created only when the component actually exposes the element.

        Older firmwares publish the reading alone - in a sample of 20 real
        installations none of them carried a setpoint. Guarding on is_enabled
        means those keep exactly the entities they have today, instead of
        gaining one that would sit at `unknown` forever.
        """
        if not component.is_enabled(SfeType.STATE_HUMIDITY_SETPOINT):
            return None
        return VimarSensor(
            id=str(component.idsf) + "_humidity_setpoint",
            name=component.name + " - " + "Humidity Setpoint",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.HUMIDITY,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.setpoint_value(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.PERCENTAGE,
            state_class=None,
            options=None,
        )

    def setpoint_value(self, component: UserComponent) -> str | Decimal | None:
        value = component.get_value(SfeType.STATE_HUMIDITY_SETPOINT)
        if value:
            return Decimal(value)
        return None

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.HUMIDITY,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.PERCENTAGE,
            state_class=None,
            options=None,
        )

    def _button_real_time(self, component: UserComponent, *args):
        return None  # Optional by Vimar

    def native_value(self, component: UserComponent) -> str | Decimal | None:
        value = component.get_value(SfeType.STATE_HUMIDITY)
        if value:
            return Decimal(value)
        return None

    def decimal_precision(self, component: UserComponent) -> int:
        return 0
