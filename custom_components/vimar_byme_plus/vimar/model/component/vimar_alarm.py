from dataclasses import dataclass

from .vimar_component import VimarComponent


@dataclass
class VimarAlarm(VimarComponent):
    """SAI alarm panel (SS_SceneActivator_Sai) as alarm_control_panel in HA."""

    @staticmethod
    def get_table_header() -> list:
        return ["Area", "Name", "Type"]

    def to_table(self) -> list:
        return [self.area, self.name, self.device_name]
