from dataclasses import dataclass

from .vimar_component import VimarComponent


@dataclass
class VimarSwitch(VimarComponent):
    main_id: str | None
    is_on: bool

    @staticmethod
    def get_table_header() -> list:
        return [
            "Area",
            "Name",
            "Type",
            "IsOn",
        ]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.is_on,
        ]
