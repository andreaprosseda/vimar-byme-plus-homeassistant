"""XML parsing utilities."""

from xml.etree.ElementTree import Element

from defusedxml.ElementTree import fromstring, parse

from ..vimar.model.byme_configuration.byme_configuration import ByMeConfiguration


def parse_config_from_path(xml_file_path: str) -> ByMeConfiguration:
    """Parse VIMAR XML Configuration from XML File Path."""
    tree = parse(xml_file_path)
    return _parse_config(tree.getroot())


def parse_config_from_file(xml: str) -> ByMeConfiguration:
    """Parse VIMAR XML Configuration from XML Content."""
    tree = fromstring(xml)
    return _parse_config(tree)


def _parse_config(element: Element) -> ByMeConfiguration:
    """Parse VIMAR XML Configuration from ElementTree."""
    return ByMeConfiguration.from_element(element)
