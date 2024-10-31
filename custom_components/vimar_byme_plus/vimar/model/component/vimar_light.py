from enum import Enum
from dataclasses import dataclass
from .vimar_component import VimarComponent
from .vimar_action import VimarAction
from ..enum.sfetype_enum import SfeType


class ColorMode(Enum):
    UNKNOWN = "unknown"
    ONOFF = "onoff"
    BRIGHTNESS = "brightness"
    COLOR_TEMP = "color_temp"
    HS = "hs"
    XY = "xy"
    RGB = "rgb"
    RGBW = "rgbw"
    RGBWW = "rgbww"
    WHITE = "white"


CMD_ON_OFF = SfeType.CMD_ON_OFF
CMD_BRIGHTNESS = SfeType.CMD_BRIGHTNESS


@dataclass
class VimarLight(VimarComponent):
    is_on: bool
    brightness: int | None
    color_mode: ColorMode | None
    hs_color: tuple[float, float] | None
    xy_color: tuple[float, float] | None
    rgb_color: tuple[int, int, int] | None
    rgbw_color: tuple[int, int, int, int] | None
    rgbww_color: tuple[int, int, int, int, int] | None
    effect_list: list[str] | None
    effect: str | None
    supported_color_modes: set[ColorMode] | None

    def get_turn_on_actions(self, brigthness: int | None = None) -> list[VimarAction]:
        """Turn the light on."""
        result = [self._get_action(CMD_ON_OFF, "On")]
        if brigthness:
            result.append(self._get_action(CMD_BRIGHTNESS, brigthness))
        return result

    def get_turn_off_actions(self) -> list[VimarAction]:
        """Turn the light off."""
        return [self._get_action(CMD_ON_OFF, "Off")]

    def _get_action(self, sfetype: SfeType, value: str) -> VimarAction:
        return VimarAction(idsf=self.id, sfetype=sfetype, value=value)

    @staticmethod
    def get_table_header() -> list:
        return ["Area", "Name", "Type", "isOn", "Brightness"]

    def to_table(self) -> list:
        return [self.area, self.name, self.device_name, self.is_on, self.brightness]
