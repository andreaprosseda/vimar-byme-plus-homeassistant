"""Group model for Vimar Configuration."""

from dataclasses import dataclass, field
from xml.etree.ElementTree import Element

from .group_address import GroupAddress


@dataclass
class Group:
    """byme_configuration.applications[].groups[] structure."""

    id: int
    label: str
    parent_id: int
    group_addresses: list[GroupAddress] = field(default_factory=list)

    def __str__(self) -> str:
        """Return string representation of this class."""
        return f"Group {self.label}, {self.group_addresses}"

    @staticmethod
    def from_element(element: Element):
        """Create an instance of this class, taking an xml Element as input."""
        return Group(
            id=element.attrib.get("id", None),
            label=element.attrib.get("label", None),
            parent_id=element.attrib.get("parentId", None),
            group_addresses=Group._get_group_addresses(element),
        )

    @staticmethod
    def _get_group_addresses(element: Element):
        group_addresses = element.find("group_addresses").findall("group_address")
        return [GroupAddress.from_element(elem) for elem in group_addresses]
