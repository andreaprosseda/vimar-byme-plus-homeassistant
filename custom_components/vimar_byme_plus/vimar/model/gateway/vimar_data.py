from dataclasses import dataclass, field

from ..component.vimar_binary_sensor import VimarBinarySensor
from ..component.vimar_button import VimarButton
from ..component.vimar_climate import VimarClimate
from ..component.vimar_component import VimarComponent
from ..component.vimar_cover import VimarCover
from ..component.vimar_light import VimarLight
from ..component.vimar_media_player import VimarMediaPlayer
from ..component.vimar_sensor import VimarSensor
from ..component.vimar_switch import VimarSwitch


@dataclass
class VimarData:
    _components: list[VimarComponent] = field(default_factory=list)

    def get_all(self) -> list[VimarComponent]:
        return [component for component in self._components if component is not None]

    def get_binary_sensors(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarBinarySensor)]

    def get_buttons(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarButton)]

    def get_climates(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarClimate)]

    def get_covers(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarCover)]

    def get_lights(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarLight)]

    def get_media_players(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarMediaPlayer)]

    def get_sensors(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarSensor)]

    def get_switches(self) -> list:
        return [ety for ety in self.get_all() if isinstance(ety, VimarSwitch)]

    def get_by_id(self, id: str) -> VimarComponent:
        for component in self.get_all():
            if component.id == id:
                return component
        return None
