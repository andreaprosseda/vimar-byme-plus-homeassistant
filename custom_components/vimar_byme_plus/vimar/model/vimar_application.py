"""Representation of a VIMAR entity."""

from enum import Enum

from .byme_configuration.application import Application
from .byme_configuration.environment import Environment


class VimarType(Enum):
    """Handled VIMAR types."""

    LIGHT = {"id": "1", "device_class": "light"}
    COVER = {"id": "2", "device_class": "cover"}
    DOOR = {"id": "9", "device_class": "door"}
    CLIMA = {"id": "4", "device_class": "climate"}

    @staticmethod
    def from_id(value: str):
        for vimar_type in VimarType:
            if vimar_type.value.get("id") == value:
                return vimar_type
        return None

    def id(self) -> str:
        """Return id of the entity."""
        return self.value.get("id")


class VimarApplication:
    """Class representation of a VIMAR entity."""

    type: VimarType
    application: Application
    environment: Environment

    def __init__(self, type: VimarType, app: Application, env: Environment) -> None:
        """Initialize Vimar Data."""
        self.type = type
        self.application = app
        self.environment = env
