from dataclasses import dataclass
from .vimar_component import VimarComponent


@dataclass
class VimarBinarySensor(VimarComponent):
    is_on: bool

    @staticmethod
    def get_table_header() -> list:
        return [
            "Area",
            "Name",
            "Type",
            "Value",
        ]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.native_value,
        ]