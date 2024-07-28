"""Environment model for Vimar Configuration."""

from dataclasses import dataclass
from xml.etree.ElementTree import Element


@dataclass
class Environment:
    """byme_configuration.environments[] structure."""

    id: int
    label: str
    parent_id: int

    def __str__(self) -> str:
        """Return string representation of this class."""
        return f"Environment {self.label}"

    @staticmethod
    def from_element(element: Element):
        """Create an instance of this class, taking an xml Element as input."""
        return Environment(
            id=element.attrib.get("id", None),
            label=element.attrib.get("label", None),
            parent_id=element.attrib.get("parentId", None),
        )
