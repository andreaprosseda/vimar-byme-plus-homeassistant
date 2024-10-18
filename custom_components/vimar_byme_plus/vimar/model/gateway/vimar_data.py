from dataclasses import dataclass, field
from ..component.vimar_component import VimarComponent
from ..component.vimar_light import VimarLight
from ..component.vimar_cover import VimarCover


@dataclass
class VimarData:
    _lights: list[VimarLight] = field(default_factory=list)
    _shutters: list[VimarCover] = field(default_factory=list)
    _access: list[VimarCover] = field(default_factory=list)
    _climates: list = field(default_factory=list)

    def get_lights(self) -> list:
        return self._lights

    def get_covers(self) -> list:
        return self._shutters + self._access

    def get_climates(self) -> list:
        return self._climates

    def get_all(self) -> list[VimarComponent]:
        return self.get_lights() + self.get_covers()

    def get_by_id(self, id) -> VimarComponent:
        for component in self.get_all():
            if component.id == id:
                return component
        return None
