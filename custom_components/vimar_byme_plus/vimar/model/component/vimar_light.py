from enum import Enum
from dataclasses import dataclass
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
    hs_color: tuple[float, float] | None
    xy_color: tuple[float, float] | None
    rgb_color: tuple[int, int, int] | None
    rgbw_color: tuple[int, int, int, int] | None
    rgbww_color: tuple[int, int, int, int, int] | None
    effect_list: list[str] | None
    effect: str | None
    supported_color_modes: set[ColorMode] | None
    
    def get_request_turn_on(self) -> None:
        pass

    def get_request_turn_off(self) -> None:
        """Turn the light off."""
        pass
    
    @staticmethod
    def get_table_header() -> list:
        return ['Area', 'Name', 'Type', 'isOn', 'Brightness']
    
    def to_table(self) -> list:
        return [self.area, self.name, self.device_name, self.is_on, self.brightness]
