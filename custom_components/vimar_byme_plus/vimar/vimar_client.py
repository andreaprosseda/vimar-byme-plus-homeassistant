"""Client interface for Vimar interactions."""

import logging

from ..utils.parse_xml import parse_config_from_path
from .model.byme_configuration.byme_configuration import ByMeConfiguration

_LOGGER = logging.getLogger(__name__)


class VimarClient:
    """Handle the communication with Vimar Gateway."""

    username: str
    password: str

    def __init__(self, data: dict[str, str]) -> None:
        """Initialize the client."""
        self.username = data.get("username")
        self.password = data.get("password")

    async def login(self) -> dict:
        """Login flow with Vimar."""
        _LOGGER.debug("Logging with Vimar credentials")
        response = {"username": "username!"}
        _LOGGER.info("Login completed")
        return response

    def get_configuration(self) -> ByMeConfiguration:
        """Mock config retrieve."""
        path = "vimar_config.xml"
        return parse_config_from_path(path)
        # return parse_config_from_file(self.get_config())

    def get_configuration_dict(self) -> dict:
        """Mock config retrieve."""
        _LOGGER.debug("Retrieving configuration")
        response = self.get_configuration()
        config = response.to_dict()
        _LOGGER.info("Configuration retrieved")
        return config