"""Config flow for VIMAR By-me Plus HUB."""

from collections.abc import Mapping
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import DOMAIN
from .coordinator import VimarDataUpdateCoordinator, VimarLoginException

_LOGGER = logging.getLogger(__name__)

USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)


class VimarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """VIMAR Config Flow."""

    VERSION = 1

    async def async_step_import(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by configuration file."""
        _LOGGER.debug("async_step_import started")
        return await self.async_step_user(user_input)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        _LOGGER.debug("async_step_user started")

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self._show_user_login_form()

        try:
            coordinator = VimarDataUpdateCoordinator(self.hass, user_input)
            response = await coordinator.retrieve_data()
            return await self._finalize(coordinator, response)
        except VimarLoginException:
            errors = {"base": "Error during login"}
            return self._show_user_login_form(errors)

    async def _finalize(self, coordinator, data: Mapping[str, Any]):
        username = coordinator.client.username
        await self.async_set_unique_id(username)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=username, data=data)

    def _show_user_login_form(self, errors=None) -> str:
        if errors:
            _LOGGER.error("Error during authentication {errors}")

        _LOGGER.debug("Showing User login form")
        return self.async_show_form(
            step_id="user", data_schema=USER_DATA_SCHEMA, errors=errors
        )
