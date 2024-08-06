"""ByMe Configuration model for Vimar Configuration."""

from dataclasses import dataclass, field
from xml.etree.ElementTree import Element

from .application import Application
from .environment import Environment


@dataclass
class ByMeConfiguration:
    """root structure."""

    environments: list[Environment] = field(default_factory=list)
    applications: list[Application] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert current class in dict."""
        return vars(self)

    @staticmethod
    def from_element(element: Element):
        """Create an instance of this class, taking an xml Element as input."""
        return ByMeConfiguration(
            environments=ByMeConfiguration._get_environments(element),
            applications=ByMeConfiguration._get_applications(element),
        )

    @staticmethod
    def _get_environments(element: Element):
        environments = element.find("environments").findall("environment")
        return [Environment.from_element(elem) for elem in environments]

    @staticmethod
    def _get_applications(element: Element):
        applications = element.find("applications").findall("application")
        return [Application.from_element(elem) for elem in applications]
