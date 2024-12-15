from dataclasses import dataclass
from .vimar_component import VimarComponent


@dataclass
class VimarButton(VimarComponent):
    main_id: str | None

    @staticmethod
    def get_table_header() -> list:
        return [
            "Area",
            "Name",
            "Type",
            "Main ID",
        ]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.main_id,
        ]
