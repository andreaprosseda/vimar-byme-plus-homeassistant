"""Dpt model for Vimar Configuration."""

from dataclasses import dataclass
from xml.etree.ElementTree import Element


@dataclass
class Dpt:
    """byme_configuration.applications[].groups[].group_addresses[].dpt structure."""

    id: str
    name: str

    def __str__(self) -> str:
        """Return string representation of this class."""
        return f"Dpt {self.name} - {self.id}"

    @staticmethod
    def from_element(element: Element):
        """Create an instance of this class, taking an xml Element as input."""
        return Dpt(
            id=element.attrib.get("id", None), name=element.attrib.get("name", None)
        )
