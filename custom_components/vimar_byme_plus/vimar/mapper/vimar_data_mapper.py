from .clima.clima_mapper import ClimaMapper
from .audio.audio_mapper import AudioMapper
from .access.access_mapper import AccessMapper
from .light.light_mapper import LightMapper
from .shutter.shutter_mapper import ShutterMapper
from .energy.energy_mapper import EnergyMapper
from .irrigation.irrigation_mapper import IrrigationMapper
from ..model.repository.user_component import UserComponent
from ..model.gateway.vimar_data import VimarData


class VimarDataMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> VimarData:
        return VimarData(
            _accesses=AccessMapper.from_list(components),
            _audios=AudioMapper.from_list(components),
            _climates=ClimaMapper.from_list(components),
            _energies=EnergyMapper.from_list(components),
            _irrigations=IrrigationMapper.from_list(components),
            _lights=LightMapper.from_list(components),
            _shutters=ShutterMapper.from_list(components),
            _switches=[]#SwitchMapper.from_list(components),
        )
