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
from homeassistant.components import zeroconf

from .const import GATEWAY_NAME, ADDRESS, GATEWAY_ID, CODE, HOST, PORT, PROTOCOL, DOMAIN
from .coordinator import Coordinator
from .vimar.model.exceptions import CodeNotValidException, VimarErrorResponseException
from .vimar.utils.logger import log_debug, log_error
from .vimar.model.gateway.gateway_info import GatewayInfo

_LOGGER = logging.getLogger(__name__)

ZEROCONF_DATA_SCHEMA = vol.Schema({
    vol.Required(CODE): str
})

USER_DATA_SCHEMA = vol.Schema({
    vol.Required(GATEWAY_NAME): str,
    vol.Required(ADDRESS): str,
    vol.Required(GATEWAY_ID): str,
    vol.Required(CODE): str,
})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    discovery_info: zeroconf.ZeroconfServiceInfo = None

    VERSION = 1

    # CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL  # CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the user manual setup."""
        step_id = "user"
        schema = USER_DATA_SCHEMA
        if user_input is not None:
            user_input = self._enhance_user_input(user_input)
            return await self._initialize(step_id, user_input, schema)
        return self.async_show_form(step_id=step_id, data_schema=schema)

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> ConfigFlowResult:
        """Handle zeroconf discovery."""
        step_id = "discovery_confirm"
        schema = ZEROCONF_DATA_SCHEMA
        self.discovery_info = discovery_info
        return self.async_show_form(step_id=step_id, data_schema=schema)

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm discovery."""
        step_id = "discovery_confirm"
        schema = ZEROCONF_DATA_SCHEMA
        if CODE in user_input:
            user_input = self._enhance_user_input(user_input)
            return await self._initialize(step_id, user_input, schema)
        return await self.async_show_form(step_id, schema)

    async def _initialize(
        self,
        step_id: str,
        data_schema: Any,
        user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Start the config flow."""
        errors = {}
        if user_input is not None:
            try:
                name = await self._finalize(user_input)
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

        return self.async_show_form(
            step_id=step_id, data_schema=data_schema, errors=errors
        )

    async def _finalize(self, user_input: dict[str, str]) -> dict[str, Any]:
        """Finalize the config flow."""
        info = self._get_gateway_info(user_input)
        coordinator = Coordinator(self.hass, info)
        coordinator.initialize(user_input)
        await self.hass.async_add_executor_job(coordinator.associate)
        return coordinator.gateway_info.plantname
    
    def _get_gateway_info(self, user_input: dict[str, str]) -> GatewayInfo:
        return GatewayInfo(
            host=user_input[HOST],
            address=user_input[ADDRESS],
            port=user_input[PORT],
            deviceuid=user_input[GATEWAY_ID],
            plantname=user_input[GATEWAY_NAME],
            protocolversion=user_input[PROTOCOL]
        )
        
    def _enhance_user_input(self, user_input: dict[str, str]) -> dict[str, str]:
        if self.discovery_info:
            new_info = self._enhance_with_discovery_info()
        else:
            new_info = self._enhance_with_default_value(user_input)
        user_input.update(new_info)
        return user_input

    
    def _enhance_with_discovery_info(self) -> dict[str, str]:
        props = self.discovery_info.properties
        return {
            HOST            : self.discovery_info.host,
            ADDRESS         : self.discovery_info.ip_address,
            PORT            : self.discovery_info.port,
            GATEWAY_ID      : props.get("deviceuid"),
            GATEWAY_NAME    : props.get("plantname"),
            PROTOCOL        : props.get("protocolversion")
        }

        
    def _enhance_with_default_value(self, user_input: dict[str, str]) -> dict[str, str]:
        return {
            HOST            : f"AG-{user_input[GATEWAY_ID]}.local.",
            ADDRESS         : user_input[ADDRESS],
            PORT            : "20615",
            GATEWAY_ID      : user_input[GATEWAY_ID],
            GATEWAY_NAME    : user_input[GATEWAY_NAME],
            PROTOCOL        : "2.7"
        }