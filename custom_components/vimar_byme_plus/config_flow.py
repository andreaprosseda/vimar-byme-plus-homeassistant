"""Config flow for VIMAR By-me Plus."""

from __future__ import annotations
from collections.abc import Mapping
from typing import Any

import logging
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.config_entries import ConfigFlowResult, SOURCE_REAUTH
from homeassistant.core import HomeAssistant

from .const import CODE, DOMAIN
from .coordinator_ import VimarDataUpdateCoordinator
from .coordinator import Coordinator
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException
from .vimar.utils.logger import log_debug, log_error

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required(CODE): str})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1

    # CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL  # CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                name = await self.finalize(user_input)
                await self.async_set_unique_id(name)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=name, data=user_input)
            except VimarErrorResponseException as err:
                errors["base"] = f"Error returned from Gateway: {err.message}"
            except CodeNotValidException:
                # Setup Code not valid. Code is 4-digit!
                errors["base"] = "invalid_code"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=DATA_SCHEMA,
            )
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict) -> dict:
        """Create an oauth config entry or update existing entry for reauth."""
        self.async_set_unique_id("user_id")
        if self.source == SOURCE_REAUTH:
            self._abort_if_unique_id_mismatch()
            return self.async_update_reload_and_abort(
                self._get_reauth_entry(),
                data_updates=data,
            )
        self._abort_if_unique_id_configured()
        return await super().async_oauth_create_entry(data)

    async def finalize(self, data: dict) -> dict[str, Any]:
        """Finalize the config flow."""

        coordinator = Coordinator(self.hass)
        coordinator.initialize(data)
        await self.hass.async_add_executor_job(coordinator.test_connection)

        return coordinator.gateway_info.plantname


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidCode(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid code."""


# class VimarConfigFlow(ConfigFlow, domain=DOMAIN):
#     """VIMAR Config Flow."""

#     VERSION = 1

#     async def async_step_user(
#         self, user_input: dict[str, Any] | None = None
#     ) -> ConfigFlowResult:
#         """Handle a flow initiated by the user."""
#         log_debug(__name__, "Method 'async_step_user' started")

#         if self._async_current_entries():
#             return self.async_abort(reason="single_instance_allowed")

#         if user_input is None:
#             log_debug(__name__, "Field 'user_input' is None, showing form...")
#             return self._show_form()

#         log_debug(__name__, "Using 'user_input' for initialization phase...")
#         return await self._initialize(user_input)

#     async def _initialize(self, user_input: dict[str, Any]) -> ConfigFlowResult:
#         log_debug(__name__, "Method '_initialize' started")
#         try:
#             coordinator = VimarDataUpdateCoordinator(self.hass)
#             await coordinator.initialize(user_input)
#             # await coordinator.start()
#             return await self._finalize(coordinator, user_input)
#         except CodeNotValidException:
#             errors = {
#                 "base": "Setup Code not valid (code is 4-digit!). Get it from Vimar Pro Menu -> Gateway -> 'i' -> Device Maintenance -> Third Parties Client",
#             }
#             return self._show_form(errors)

#     async def _finalize(
#         self, coordinator: VimarDataUpdateCoordinator, user_input: dict[str, Any]
#     ) -> ConfigFlowResult:
#         log_debug(__name__, "Method '_finalize' started")
#         name = coordinator.gateway_info.plantname
#         await self.async_set_unique_id(name)
#         self._abort_if_unique_id_configured()
#         return self.async_create_entry(title=name, data=user_input)

#     def _show_form(self, errors=None) -> ConfigFlowResult:
#         log_debug(__name__, "Method '_show_form' started")
#         if errors:
#             log_error(__name__, f"Error during flow: {errors}")

#         log_debug(__name__, "Showing User login form")
#         return self.async_show_form(
#             step_id="user", data_schema=DATA_SCHEMA, errors=errors
#         )
