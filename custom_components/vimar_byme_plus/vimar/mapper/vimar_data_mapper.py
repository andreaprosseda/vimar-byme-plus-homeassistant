from ..model.gateway.vimar_data import VimarData
from ..model.repository.user_component import UserComponent
from .access.access_mapper import AccessMapper
from .audio.audio_mapper import AudioMapper
from .automation.automation_mapper import AutomationMapper
from .clima.clima_mapper import ClimaMapper
from .energy.energy_mapper import EnergyMapper
from .irrigation.irrigation_mapper import IrrigationMapper
from .light.light_mapper import LightMapper
from .scene.scene_mapper import SceneMapper
from .scene_activator.scene_activator_mapper import SceneActivatorMapper
from .sensor.sensor_mapper import SensorMapper
from .shutter.shutter_mapper import ShutterMapper


class VimarDataMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> VimarData:
        vimar_components = []
        vimar_components.extend(AccessMapper.from_list(components))
        vimar_components.extend(AudioMapper.from_list(components))
        vimar_components.extend(AutomationMapper.from_list(components))
        vimar_components.extend(ClimaMapper.from_list(components))
        vimar_components.extend(EnergyMapper.from_list(components))
        vimar_components.extend(IrrigationMapper.from_list(components))
        vimar_components.extend(LightMapper.from_list(components))
        vimar_components.extend(SceneMapper.from_list(components))
        vimar_components.extend(SceneActivatorMapper.from_list(components))
        vimar_components.extend(SensorMapper.from_list(components))
        vimar_components.extend(ShutterMapper.from_list(components))
        return VimarData(vimar_components)
