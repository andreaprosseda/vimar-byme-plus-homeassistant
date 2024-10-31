from enum import Enum
from dataclasses import dataclass
from .vimar_component import VimarComponent
from .vimar_action import VimarAction
from ..enum.sfetype_enum import SfeType
from ..enum.sstype_enum import SsType


class CoverEntityFeature(Enum):
    OPEN = 1
    CLOSE = 2
    SET_POSITION = 4
    STOP = 8
    OPEN_TILT = 16
    CLOSE_TILT = 32
    STOP_TILT = 64
    SET_TILT_POSITION = 128


CMD_ON_OFF = SfeType.CMD_ON_OFF
CMD_SHUTTER = SfeType.CMD_SHUTTER
CMD_SHUTTER_WITHOUT_POSITION = SfeType.CMD_SHUTTER_WITHOUT_POSITION
# CMD_SLAT = SfeType.CMD_SLAT
# CMD_SLAT_WITHOUT_POSITION = SfeType.CMD_SLAT_WITHOUT_POSITION


@dataclass
class VimarCover(VimarComponent):
    current_cover_position: int | None
    is_closed: bool | None
    is_closing: bool | None
    is_opening: bool | None
    supported_features: list[CoverEntityFeature]

    def get_open_cover_actions(self) -> list[VimarAction]:
        """Open the cover."""
        print(self.device_group)
        if self.device_group == "SF_Access":
            return [self._get_action(CMD_ON_OFF, "On")]
        if self.device_name == SsType.SHUTTER_POSITION.value:
            return [self._get_action(CMD_SHUTTER, "0")]
        if self.device_name == SsType.SHUTTER_WITHOUT_POSITION.value:
            return [self._get_action(CMD_SHUTTER_WITHOUT_POSITION, "Up")]
        return []

    def get_close_cover_actions(self) -> list[VimarAction]:
        """Close cover."""
        if self.device_group == "SF_Access":
            return [self._get_action(CMD_ON_OFF, "Off")]
        if self.device_name == SsType.SHUTTER_POSITION.value:
            return [self._get_action(CMD_SHUTTER, "100")]
        if self.device_name == SsType.SHUTTER_WITHOUT_POSITION.value:
            return [self._get_action(CMD_SHUTTER_WITHOUT_POSITION, "Down")]
        return []

    def get_set_cover_position_actions(self, position: str) -> list[VimarAction]:
        """Move the cover to a specific position."""
        if self.device_name == SsType.SHUTTER_POSITION.value:
            return [self._get_action(CMD_SHUTTER, position)]
        return []

    def get_stop_cover_actions(self) -> list[VimarAction]:
        """Stop the cover."""
        if self.device_name == SsType.SHUTTER_POSITION.value:
            return [self._get_action(CMD_SHUTTER, "Stop")]
        if self.device_name == SsType.SHUTTER_WITHOUT_POSITION.value:
            return [self._get_action(CMD_SHUTTER_WITHOUT_POSITION, "Stop")]
        return []

    @staticmethod
    def get_table_header() -> list:
        return [
            "Area",
            "Name",
            "Type",
            "Position",
            "isClosed",
            "isOpening",
            "isClosing",
        ]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.current_cover_position,
            self.is_closed,
            self.is_opening,
            self.is_closing,
        ]
