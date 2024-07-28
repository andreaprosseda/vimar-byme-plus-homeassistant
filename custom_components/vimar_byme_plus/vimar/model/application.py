"""Application model for Vimar Configuration."""

from dataclasses import dataclass, field
from xml.etree.ElementTree import Element

from .group import Group


@dataclass
class Application:
    """byme_configuration.applications[] structure."""

    id: str
    label: str
    environment_id: str
    category_id: int
    category: str
    channel_id: str
    channel: str
    groups: list[Group] = field(default_factory=list)

    def __str__(self) -> str:
        """Return string representation of this class."""
        return f"\nApplication CategoryID: {self.category_id} - ChannelID: {self.channel_id} - {self.label} [{self.channel}]"

    def __repr__(self) -> str:
        """Return string representation of this class."""
        return self.__str__()

    @staticmethod
    def from_element(element: Element):
        """Create an instance of this class, taking an xml Element as input."""

        return Application(
            id=element.attrib.get("id", None),
            label=element.attrib.get("label", None),
            environment_id=element.attrib.get("environment_id", None),
            category_id=element.attrib.get("category_id", None),
            category=element.attrib.get("category", None),
            channel_id=element.attrib.get("channel_id", None),
            channel=element.attrib.get("channel", None),
            groups=Application._get_groups(element),
        )

    @staticmethod
    def _get_groups(element: Element):
        groups = element.find("groups").findall("group")
        return [Group.from_element(elem) for elem in groups]
