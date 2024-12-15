from decimal import Decimal
from ...model.component.vimar_binary_sensor import VimarBinarySensor
from ...model.component.vimar_sensor import VimarSensor, SensorDeviceClass
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSensorWeatherStationMapper:
    SSTYPE = SsType.SENSOR_WEATHER_STATION.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarBinarySensor]:
        return [
            self._night_from_obj(component),
            self._raining_from_obj(component),
            self._luminosity_from_obj(component),
            self._temperature_from_obj(component),
            self._wind_from_obj(component),
        ]

    def _night_from_obj(self, component: UserComponent) -> VimarBinarySensor:
        value = component.get_value(SfeType.STATE_ITS_NIGHT)
        return VimarBinarySensor(
            id=str(component.idsf) + "_day_night",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="light",
            area=component.ambient.name,
            is_on=value == "Day" if value else False,
        )

    def _raining_from_obj(self, component: UserComponent) -> VimarBinarySensor:
        value = component.get_value(SfeType.STATE_ITS_RAINING)
        return VimarBinarySensor(
            id=str(component.idsf) + "_raining",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="moisture",
            area=component.ambient.name,
            is_on=value == "Raining" if value else False,
        )

    def _luminosity_from_obj(self, component: UserComponent) -> VimarSensor:
        sfetype = SfeType.STATE_LUMINOSITY
        return VimarSensor(
            id=str(component.idsf) + "_luminosity",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ILLUMINANCE,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self._native_value(component, sfetype),
            last_update=None,
            decimal_precision=self._decimal_precision(component),
            unit_of_measurement=None,
            state_class=None,
            options=None,
        )

    def _temperature_from_obj(self, component: UserComponent) -> VimarSensor:
        sfetype = SfeType.STATE_SENSOR_TEMPERATURE
        return VimarSensor(
            id=str(component.idsf) + "_temperature",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.TEMPERATURE,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self._native_value(component, sfetype),
            last_update=None,
            decimal_precision=self._decimal_precision(component),
            unit_of_measurement=None,
            state_class=None,
            options=None,
        )

    def _wind_from_obj(self, component: UserComponent) -> VimarSensor:
        sfetype = SfeType.STATE_WIND_SPEED
        return VimarSensor(
            id=str(component.idsf) + "_wind_speed",
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.WIND_SPEED,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self._native_value(component, sfetype),
            last_update=None,
            decimal_precision=self._decimal_precision(component),
            unit_of_measurement=None,
            state_class=None,
            options=None,
        )

    def _native_value(
        self, component: UserComponent, sfetype: SfeType
    ) -> str | Decimal | None:
        value = component.get_value(sfetype)
        if value:
            return Decimal(value)
        return None

    def _decimal_precision(self, component: UserComponent) -> int:
        return 1
