from dataclasses import dataclass
from enum import Enum

from .vimar_component import VimarComponent


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


@dataclass
class VimarLight(VimarComponent):
    is_on: bool
    brightness: int | None
    color_mode: ColorMode | None
    hsv_color: tuple[int, int, int] | None
    rgb_color: tuple[int, int, int] | None
    temp_color: int | None
    supported_color_modes: set[ColorMode] | None

    @staticmethod
    def get_table_header() -> list:
        return ["Area", "Name", "Type", "isOn", "Brightness"]

    def to_table(self) -> list:
        return [self.area, self.name, self.device_name, self.is_on, self.brightness]
