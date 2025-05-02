"""Config flow for VIMAR By-me Plus."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import zeroconf
from homeassistant.config_entries import ConfigFlowResult

from .const import (
    ADDRESS,
    CODE,
    DOMAIN,
    GATEWAY_ID,
    GATEWAY_MODEL,
    GATEWAY_NAME,
    HOST,
    PORT,
    PROTOCOL,
)
from .coordinator import Coordinator
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException
from .vimar.utils.logger import log_debug, log_error

ZEROCONF_DATA_SCHEMA = vol.Schema({vol.Required(CODE): str})

USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(GATEWAY_NAME): str,
        vol.Required(ADDRESS): str,
        vol.Required(GATEWAY_ID): str,
        vol.Required(CODE): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    discovery_info: zeroconf.ZeroconfServiceInfo = None

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the user manual setup."""
        step_id = "user"
        schema = USER_DATA_SCHEMA
        if user_input is not None:
            user_input = self._enhance_user_input(user_input)
            await self.async_set_unique_id(user_input[GATEWAY_ID])
            self._abort_if_unique_id_configured()
            return await self._initialize(step_id, schema, user_input)
        return self.async_show_form(step_id=step_id, data_schema=schema)

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> ConfigFlowResult:
        """Handle zeroconf discovery."""
        user_input = self._get_discovery_info_as_user_input(discovery_info)
        await self.async_set_unique_id(user_input[GATEWAY_ID])
        self._abort_if_unique_id_configured()
        if user_input[GATEWAY_MODEL] != "AG+":
            return self.async_abort(reason="invalid_device")

        step_id = "discovery_confirm"
        schema = ZEROCONF_DATA_SCHEMA
        self.discovery_info = discovery_info

        placeholders = {"name": user_input[GATEWAY_NAME]}
        self.context["title_placeholders"] = placeholders

        return self.async_show_form(step_id=step_id, data_schema=schema)

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm discovery."""
        step_id = "discovery_confirm"
        schema = ZEROCONF_DATA_SCHEMA
        if user_input and CODE in user_input:
            user_input = self._enhance_user_input(user_input)
            return await self._initialize(step_id, schema, user_input)
        return self.async_show_form(step_id=step_id, data_schema=schema)

    async def _initialize(
        self, step_id: str, data_schema: Any, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Start the config flow."""
        errors = {}
        if user_input is not None:
            try:
                log_debug(__name__, user_input)
                return await self._finalize(user_input)
            except VimarErrorResponseException as err:
                errors["base"] = f"Error returned from Gateway: {err.message}"
            except CodeNotValidException:
                errors["base"] = "invalid_code"
            except Exception:  # pylint: disable=broad-except
                log_error("Unexpected exception during the finalization phase")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id=step_id, data_schema=data_schema, errors=errors
        )

    async def _finalize(self, user_input: dict[str, str]) -> ConfigFlowResult:
        """Finalize the config flow."""
        coordinator = Coordinator(self.hass, user_input)
        await self.hass.async_add_executor_job(coordinator.associate)
        title = user_input[GATEWAY_NAME]
        user_input.pop(CODE)
        return self.async_create_entry(title=title, data=user_input)

    def _enhance_user_input(self, user_input: dict[str, str]) -> dict[str, str]:
        if self.discovery_info:
            new_info = self._get_discovery_info_as_user_input(self.discovery_info)
        else:
            new_info = self._get_default_value_as_user_input(user_input)
        user_input.update(new_info)
        return user_input

    def _get_discovery_info_as_user_input(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> dict[str, str]:
        props = discovery_info.properties
        return {
            HOST: discovery_info.hostname.replace(".local.", ""),
            ADDRESS: str(discovery_info.ip_address),
            PORT: discovery_info.port,
            GATEWAY_ID: props.get("deviceuid"),
            GATEWAY_MODEL: props.get("model"),
            GATEWAY_NAME: props.get("plantname"),
            PROTOCOL: props.get("protocolversion"),
        }

    def _get_default_value_as_user_input(
        self, user_input: dict[str, str]
    ) -> dict[str, str]:
        return {
            HOST: f"AG-{user_input[GATEWAY_ID]}",
            ADDRESS: user_input[ADDRESS],
            PORT: "20615",
            GATEWAY_ID: user_input[GATEWAY_ID],
            GATEWAY_MODEL: "AG+",
            GATEWAY_NAME: user_input[GATEWAY_NAME],
            PROTOCOL: "2.7",
        }
