from dataclasses import dataclass, field
from ..component.vimar_component import VimarComponent
from ..component.vimar_light import VimarLight
from ..component.vimar_cover import VimarCover
from ..component.vimar_climate import VimarClimate
from ..component.vimar_media_player import VimarMediaPlayer
from ..component.vimar_sensor import VimarSensor


@dataclass
class VimarData:
    _lights: list[VimarLight] = field(default_factory=list)
    _shutters: list[VimarCover] = field(default_factory=list)
    _access: list[VimarCover] = field(default_factory=list)
    _climates: list[VimarClimate] = field(default_factory=list)
    _audios: list[VimarMediaPlayer] = field(default_factory=list)
    _energies: list[VimarSensor] = field(default_factory=list)

    def get_lights(self) -> list:
        return self._lights

    def get_covers(self) -> list:
        return self._shutters + self._access

    def get_climates(self) -> list:
        return self._climates

    def get_audios(self) -> list:
        return self._audios

    def get_sensors(self) -> list:
        return self._energies

    def get_all(self) -> list[VimarComponent]:
        return (
            self.get_lights()
            + self.get_covers()
            + self.get_climates()
            + self.get_audios()
            + self.get_sensors()
        )

    def get_by_id(self, id: str) -> VimarComponent:
        for component in self.get_all():
            if component.id == id:
                return component
        return None
