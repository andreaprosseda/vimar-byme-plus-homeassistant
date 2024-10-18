from dataclasses import dataclass
from .vimar_component import VimarComponent

@dataclass
class VimarLight(VimarComponent):
    is_on: bool
    brightness: int | None
    color_mode: str | None
    hs_color: tuple[float, float] | None
    xy_color: tuple[float, float] | None
    rgb_color: tuple[int, int, int] | None
    rgbw_color: tuple[int, int, int, int] | None
    rgbww_color: tuple[int, int, int, int, int] | None
    effect_list: list[str] | None
    effect: str | None
    supported_color_modes: set[str] | None
    
    def __repr__(self) -> str:
        return f"[Light] [{self.area}] {self.name} - {'On' if self.is_on else 'Off'}"

    def get_request_turn_on(self) -> None:
        pass

    def get_request_turn_off(self) -> None:
        """Turn the light off."""
        pass