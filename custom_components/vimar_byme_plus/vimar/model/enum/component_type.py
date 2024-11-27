from enum import Enum


class ComponentType(Enum):
    LIGHT = {"sftype": "SF_Light"}
    ENERGY = {"sftype": "SF_Energy"}
    CLIMA = {"sftype": "SF_Clima"}
    COVER = {"sftype": "SF_Shutter"}
    DOOR = {"sftype": "SF_Access"}
    AUDIO = {"sftype": "SF_Audio"}

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
