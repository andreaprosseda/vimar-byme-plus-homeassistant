from dataclasses import dataclass
from .vimar_component import VimarComponent

@dataclass
class VimarCover(VimarComponent):
    current_cover_position: int | None
    is_closed: bool | None
    is_closing: bool | None
    is_opening: bool | None
    
    def __repr__(self) -> str:
        return f"[Cover] [{self.area}] {self.name} - {self.current_cover_position}%"
    
    def get_request_open_cover(self) -> None:
        """Open the cover."""
        raise NotImplementedError

    def get_request_close_cover(self) -> None:
        """Close cover."""
        pass

    def get_request_set_cover_position(self) -> None:
        """Move the cover to a specific position."""
        pass
    
    def get_request_stop_cover(self) -> None:
        """Stop the cover."""
        pass
