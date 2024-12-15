from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_sensor_air_quality_gradient_mapper import SsSensorAirQualityGradientMapper
from .ss_sensor_humidity_mapper import SsSensorHumidityMapper
from .ss_sensor_interface_contact_mapper import SsSensorInterfaceContactMapper
from .ss_sensor_weather_station_mapper import SsSensorWeatherStationMapper


class SensorMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.SENSOR.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [SensorMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = SensorMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsSensorAirQualityGradientMapper.SSTYPE:
            return SsSensorAirQualityGradientMapper()
        if sstype == SsSensorHumidityMapper.SSTYPE:
            return SsSensorHumidityMapper()
        if sstype == SsSensorInterfaceContactMapper.SSTYPE:
            return SsSensorInterfaceContactMapper()
        if sstype == SsSensorWeatherStationMapper.SSTYPE:
            return SsSensorWeatherStationMapper()
        raise NotImplementedError
