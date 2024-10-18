"""Config flow for VIMAR By-me Plus HUB."""

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CODE, DOMAIN
from .coordinator import VimarDataUpdateCoordinator
from .vimar.model.exception.code_not_valid_exception import CodeNotValidException
from .vimar.utils.logger import log_debug, log_error

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CODE): str,
    }
)


class VimarConfigFlow(ConfigFlow, domain=DOMAIN):
    """VIMAR Config Flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        log_debug(__name__, "Method 'async_step_user' started")

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            log_debug(__name__, "Field 'user_input' is None, showing form...")
            return self._show_form()

        log_debug(__name__, "Using 'user_input' for initialization phase...")
        return await self._initialize(user_input)

    async def _initialize(self, user_input: dict[str, Any]) -> ConfigFlowResult:
        log_debug(__name__, "Method '_initialize' started")
        try:
            coordinator = VimarDataUpdateCoordinator(self.hass)
            await coordinator.initialize(user_input)
            # await coordinator.start()
            return await self._finalize(coordinator, user_input)
        except CodeNotValidException:
            errors = {
                "base": "Setup Code not valid (code is 4-digit!). Get it from Vimar Pro Menu -> Gateway -> 'i' -> Device Maintenance -> Third Parties Client",
            }
            return self._show_form(errors)

    async def _finalize(
        self, coordinator: VimarDataUpdateCoordinator, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        log_debug(__name__, "Method '_finalize' started")
        name = coordinator.gateway_info.plantname
        await self.async_set_unique_id(name)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=name, data=user_input)

    def _show_form(self, errors=None) -> ConfigFlowResult:
        log_debug(__name__, "Method '_show_form' started")
        if errors:
            log_error(__name__, f"Error during flow: {errors}")

        log_debug(__name__, "Showing User login form")
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
