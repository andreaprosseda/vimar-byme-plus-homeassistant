from enum import Enum


class ComponentType(Enum):
    LIGHT = {"sftype": "SF_Light", "device_class": "light"}
    ENERGY = {"sftype": "SF_Energy", "device_class": "energy"}
    CLIMA = {"sftype": "SF_Clima", "device_class": "climate"}
    COVER = {"sftype": "SF_Shutter", "device_class": "cover"}
    DOOR = {"sftype": "SF_Access", "device_class": "door"}
    AUDIO = {"sftype": "SF_Audio", "device_class": "media_player"}

    @staticmethod
    def from_type(value: str):
        for component_type in ComponentType:
            if component_type.value.get("sftype") == value:
                return component_type
        return None

    def id(self) -> str:
        """Return id of the entity."""
        return self.value.get("sftype")

    def device_class(self) -> str:
        """Return id of the entity."""
        return self.value.get("device_class")
