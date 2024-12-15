from dataclasses import dataclass, field
from ..component.vimar_component import VimarComponent
from ..component.vimar_light import VimarLight
from ..component.vimar_button import VimarButton
from ..component.vimar_cover import VimarCover
from ..component.vimar_climate import VimarClimate
from ..component.vimar_media_player import VimarMediaPlayer
from ..component.vimar_sensor import VimarSensor
from ..component.vimar_switch import VimarSwitch


@dataclass
class VimarData:
    _automations: list[VimarSwitch] = field(default_factory=list)
    _accesses: list[VimarCover] = field(default_factory=list)
    _audios: list[VimarMediaPlayer] = field(default_factory=list)
    _climates: list[VimarClimate] = field(default_factory=list)
    _energies: list[VimarSensor] = field(default_factory=list)
    _lights: list[VimarLight] = field(default_factory=list)
    _shutters: list[VimarCover] = field(default_factory=list)
    _irrigations: list[VimarComponent] = field(default_factory=list)

    def get_all(self) -> list[VimarComponent]:
        return (
            self.get_buttons()
            + self.get_climates()
            + self.get_covers()
            + self.get_lights()
            + self.get_media_players()
            + self.get_sensors()
            + self.get_switches()
        )

    def get_buttons(self) -> list:
        return self._get_irrigation_buttons()

    def get_climates(self) -> list:
        return []  # self._climates

    def get_covers(self) -> list:
        return []  # self._shutters + self._accesses

    def get_lights(self) -> list:
        return []  # self._lights

    def get_media_players(self) -> list:
        return []  # self._audios

    def get_sensors(self) -> list:
        return self._energies + self._get_irrigation_sensors()

    def get_switches(self) -> list:
        return self._automations + self._get_irrigation_switches()

    def _get_irrigation_buttons(self) -> list[VimarButton]:
        return [ety for ety in self._irrigations if isinstance(ety, VimarButton)]

    def _get_irrigation_sensors(self) -> list[VimarSensor]:
        return [ety for ety in self._irrigations if isinstance(ety, VimarSensor)]

    def _get_irrigation_switches(self) -> list[VimarSwitch]:
        return [ety for ety in self._irrigations if isinstance(ety, VimarSwitch)]

    def get_by_id(self, id: str) -> VimarComponent:
        for component in self.get_all():
            if component.id == id:
                return component
        return None
