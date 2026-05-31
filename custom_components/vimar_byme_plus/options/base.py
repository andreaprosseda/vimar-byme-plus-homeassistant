"""Base abstraction for OptionsFlow sections.

Each section is an independent unit of configuration with its own form,
storage slot in `entry.options`, and applicability predicate. Sections are
composed by the OptionsFlow at runtime: only those whose `is_applicable`
returns True are exposed to the user.

Adding a new section requires:
  1. a subclass of `OptionsSection` in this package,
  2. registration in `options/__init__.py` (`SECTIONS` tuple),
  3. an `async_step_<section_id>` method on `OptionsFlowHandler`
     delegating to `_handle_section_step`,
  4. translation entries under `options.step.<section_id>` and a label
     under `options.step.init.menu_options.<section_id>`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant


class OptionsSection(ABC):
    """A configurable section in the OptionsFlow."""

    id: str  # unique id, also key under entry.options

    @abstractmethod
    async def is_applicable(self, hass: HomeAssistant) -> bool:
        """Return True if this section has anything to configure right now."""

    @abstractmethod
    async def build_schema(
        self, hass: HomeAssistant, current: dict[str, Any]
    ) -> vol.Schema:
        """Return the form schema, pre-populated with current values."""

    async def description_placeholders(
        self, hass: HomeAssistant
    ) -> dict[str, str] | None:
        """Optional description placeholders shown in the form's text."""
        return None

    async def transform_user_input(
        self, hass: HomeAssistant, user_input: dict[str, Any]
    ) -> dict[str, Any]:
        """Optional hook to post-process user input before persisting."""
        return user_input
