from ...model.component.vimar_binary_sensor import VimarBinarySensor
from ...model.component.vimar_component import VimarComponent
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_sensor_generic_mapper import SsSensorGenericMapper
from .ss_sensor_luminosity_mapper import SsSensorLuminosityMapper
from .ss_sensor_temperature_mapper import SsSensorTemperatureMapper
from .ss_sensor_wind_speed_mapper import SsSensorWindSpeedMapper


class SsSensorWeatherStationMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_WEATHER_STATION.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarComponent]:
        values = []
        values.append(self._night_from_obj(component))
        values.append(self._raining_from_obj(component))

        values.extend(self._luminosity_from_obj(component))
        values.extend(self._temperature_from_obj(component))
        values.extend(self._wind_from_obj(component))
        return values

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

    def _luminosity_from_obj(self, component: UserComponent) -> list[VimarComponent]:
        custom_id = str(component.idsf) + "_luminosity"
        return SsSensorLuminosityMapper().from_obj(component, custom_id)

    def _temperature_from_obj(self, component: UserComponent) -> list[VimarComponent]:
        custom_id = str(component.idsf) + "_temperature"
        return SsSensorTemperatureMapper().from_obj(component, custom_id)

    def _wind_from_obj(self, component: UserComponent) -> list[VimarComponent]:
        custom_id = str(component.idsf) + "_wind_speed"
        return SsSensorWindSpeedMapper().from_obj(component, custom_id)
