from dataclasses import dataclass


@dataclass
class VimarComponent:
    id: str
    name: str
    device_name: str
    area: str
    
    @staticmethod
    def get_table_header() -> list:
        return ['Area', 'Name']
    
    def to_table(self) -> list:
        return [self.area, self.name]
