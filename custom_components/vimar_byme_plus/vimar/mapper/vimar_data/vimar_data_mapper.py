from .clima_mapper import ClimaMapper
from .access_mapper import AccessMapper
from .light_mapper.light_mapper import LightMapper
from .shutter_mapper.shutter_mapper import ShutterMapper
from .audio_mapper.audio_mapper import AudioMapper
from ...model.repository.user_component import UserComponent
from ...model.gateway.vimar_data import VimarData
class VimarDataMapper:

    @staticmethod    
    def from_list(components: list[UserComponent]) -> VimarData:
        return VimarData(
            _lights = LightMapper.from_list(components),
            _shutters = ShutterMapper.from_list(components),
            _access = AccessMapper.from_list(components),
            _climates = ClimaMapper.from_list(components),
            _audios = AudioMapper.from_list(components)
        )