"""GroupAddress model for Vimar Configuration."""

from dataclasses import dataclass
from xml.etree.ElementTree import Element

from .dpt import Dpt


@dataclass
class GroupAddress:
    """byme_configuration.applications[].groups[].group_addresses structure."""

    address: str
    flags: str
    dpt: Dpt
    dptx: Dpt

    @staticmethod
    def from_element(element: Element):
        """Create an instance of this class, taking an xml Element as input."""
        return GroupAddress(
            address=element.attrib.get("address", None),
            flags=element.attrib.get("flags", None),
            dpt=GroupAddress._get_dpt(element),
            dptx=GroupAddress._get_dptx(element),
        )

    @staticmethod
    def _get_dpt(element: Element):
        dpt = element.find("dpt")
        return Dpt.from_element(dpt)

    @staticmethod
    def _get_dptx(element: Element):
        dptx = element.find("dptx")
        return Dpt.from_element(dptx)
