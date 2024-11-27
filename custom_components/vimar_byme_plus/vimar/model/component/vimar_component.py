from dataclasses import dataclass


@dataclass
class VimarComponent:
    id: str
    name: str
    device_group: str
    device_name: str
    device_class: str
    area: str

    @staticmethod
    def get_table_header() -> list:
        return ["Area", "Name", "Class"]

    def to_table(self) -> list:
        return [self.area, self.name, self.device_class]
