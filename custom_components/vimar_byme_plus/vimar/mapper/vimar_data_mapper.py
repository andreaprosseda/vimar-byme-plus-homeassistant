from ..model.gateway.vimar_data import VimarData
from ..model.repository.user_component import UserComponent
from .access.access_mapper import AccessMapper
from .audio.audio_mapper import AudioMapper
from .automation.automation_mapper import AutomationMapper
from .clima.clima_mapper import ClimaMapper
from .energy.energy_mapper import EnergyMapper
from .irrigation.irrigation_mapper import IrrigationMapper
from .light.light_mapper import LightMapper
from .shutter.shutter_mapper import ShutterMapper


class VimarDataMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> VimarData:
        return VimarData(
            _automations=AutomationMapper.from_list(components),
            _accesses=AccessMapper.from_list(components),
            _audios=AudioMapper.from_list(components),
            _climates=ClimaMapper.from_list(components),
            _energies=EnergyMapper.from_list(components),
            _irrigations=IrrigationMapper.from_list(components),
            _lights=LightMapper.from_list(components),
            _shutters=ShutterMapper.from_list(components),
        )
