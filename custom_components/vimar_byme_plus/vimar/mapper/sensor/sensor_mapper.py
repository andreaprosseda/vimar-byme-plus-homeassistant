from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_sensor_air_quality_gradient_mapper import SsSensorAirQualityGradientMapper
from .ss_sensor_air_quality_mapper import SsSensorAirQualityMapper
from .ss_sensor_current_mapper import SsSensorCurrentMapper
from .ss_sensor_generic_mapper import SsSensorGenericMapper
from .ss_sensor_humidity_mapper import SsSensorHumidityMapper
from .ss_sensor_interface_contact_mapper import SsSensorInterfaceContactMapper
from .ss_sensor_luminosity_mapper import SsSensorLuminosityMapper
from .ss_sensor_power_mapper import SsSensorPowerMapper
from .ss_sensor_pressure_mapper import SsSensorPressureMapper
from .ss_sensor_rain_amount_mapper import SsSensorRainAmountMapper
from .ss_sensor_temperature_mapper import SsSensorTemperatureMapper
from .ss_sensor_tension_mapper import SsSensorTensionMapper
from .ss_sensor_volume_flow_mapper import SsSensorVolumeFlowMapper
from .ss_sensor_weather_station_mapper import SsSensorWeatherStationMapper
from .ss_sensor_wind_speed_mapper import SsSensorWindSpeedMapper


class SensorMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.SENSOR.value
        sensors = [component for component in components if component.sftype == sftype]
        components = [SensorMapper.from_obj(sensor) for sensor in sensors]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = SensorMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(__name__, component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsSensorAirQualityMapper.SSTYPE:
            return SsSensorAirQualityMapper()
        if sstype == SsSensorAirQualityGradientMapper.SSTYPE:
            return SsSensorAirQualityGradientMapper()
        if sstype == SsSensorCurrentMapper.SSTYPE:
            return SsSensorCurrentMapper()
        if sstype == SsSensorGenericMapper.SSTYPE:
            return SsSensorGenericMapper()
        if sstype == SsSensorHumidityMapper.SSTYPE:
            return SsSensorHumidityMapper()
        if sstype == SsSensorInterfaceContactMapper.SSTYPE:
            return SsSensorInterfaceContactMapper()
        if sstype == SsSensorLuminosityMapper.SSTYPE:
            return SsSensorLuminosityMapper()
        if sstype == SsSensorPowerMapper.SSTYPE:
            return SsSensorPowerMapper()
        if sstype == SsSensorPressureMapper.SSTYPE:
            return SsSensorPressureMapper()
        if sstype == SsSensorRainAmountMapper.SSTYPE:
            return SsSensorRainAmountMapper()
        if sstype == SsSensorTemperatureMapper.SSTYPE:
            return SsSensorTemperatureMapper()
        if sstype == SsSensorTensionMapper.SSTYPE:
            return SsSensorTensionMapper()
        if sstype == SsSensorVolumeFlowMapper.SSTYPE:
            return SsSensorVolumeFlowMapper()
        if sstype == SsSensorWeatherStationMapper.SSTYPE:
            return SsSensorWeatherStationMapper()
        if sstype == SsSensorWindSpeedMapper.SSTYPE:
            return SsSensorWindSpeedMapper()
        raise NotImplementedError
