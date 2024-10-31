from dataclasses import dataclass
from .vimar_action import VimarAction
from ..enum.sfetype_enum import SfeType


@dataclass
class VimarComponent:
    id: str
    name: str
    device_group: str
    device_name: str
    area: str

    @staticmethod
    def get_table_header() -> list:
        return ["Area", "Name"]

    def to_table(self) -> list:
        return [self.area, self.name]

    def _get_action(self, sfetype: SfeType, value: str) -> VimarAction:
        return VimarAction(idsf=self.id, sfetype=sfetype, value=value)
