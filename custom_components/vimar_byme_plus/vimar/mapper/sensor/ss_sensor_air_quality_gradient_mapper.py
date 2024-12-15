from ...model.component.vimar_sensor import SensorDeviceClass, VimarSensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSensorAirQualityGradientMapper:
    SSTYPE = SsType.SENSOR_AIR_QUALITY_GRADIENT.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ENUM,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=None,
            unit_of_measurement=None,
            state_class=None,
            options=self.get_values(component),
        )

    def native_value(self, component: UserComponent) -> str | None:
        value = component.get_value(SfeType.STATE_AIR_QUALITY_GRADIENT)
        return value

    def get_values(self, component: UserComponent) -> list[str]:
        # values from -2 to 2
        return [str(value) for value in range(-2, 3)]
