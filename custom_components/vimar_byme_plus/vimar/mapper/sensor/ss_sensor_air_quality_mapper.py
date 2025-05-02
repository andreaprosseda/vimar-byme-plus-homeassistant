from ...model.component.vimar_sensor import SensorDeviceClass, VimarSensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_sensor_generic_mapper import SsSensorGenericMapper


class SsSensorAirQualityMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_AIR_QUALITY.value

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.AQI,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=None,
            state_class=None,
            options=None,
        )

    def native_value(self, component: UserComponent) -> str | None:
        value = component.get_value(SfeType.STATE_AIR_QUALITY)
        return value

    def decimal_precision(self, component: UserComponent) -> int:
        return 1
