"""Client interface for Vimar interactions."""

import logging

from ..utils.parse_xml import parse_config_from_file
from .vimar_config import CONFIG

_LOGGER = logging.getLogger(__name__)


class VimarClient:
    """Handle the communication with Vimar Gateway."""

    username: str
    password: str

    def __init__(self, data: dict[str, str]) -> None:
        """Initialize the client."""
        self.username = data.get("username")
        self.password = data.get("password")

    async def login(self):
        """Login flow with Vimar."""
        _LOGGER.debug("Logging with Vimar credentials")
        response = {"username": "username!"}
        _LOGGER.info("Login completed")
        return response

    def get_configuration(self):
        """Mock config retrieve."""
        # path = "/workspaces/core/homeassistant/components/vimar/data/vimar_config.xml"
        # return parse_config(path)
        return parse_config_from_file(self.get_config())

    def get_configuration_dict(self):
        """Mock config retrieve."""
        _LOGGER.debug("Retrieving configuration")
        response = self.get_configuration()
        config = response.to_dict()
        _LOGGER.info("Configuration retrieved")
        return config

    def get_config(self):
        return CONFIG