"""OptionsFlow section: global tolerance for slat-induced position jitter.

This exposes a single integer percent (0-100). The value is stored under
entry.options[SECTION_TILT_TOLERANCE] as a plain int.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from ..const import SECTION_TILT_TOLERANCE
from .base import OptionsSection


_MIN = 0
_MAX = 100
_STEP = 1


class TiltToleranceSection(OptionsSection):
    """Global tolerance for treating near-closed positions as closed."""

    id = SECTION_TILT_TOLERANCE

    async def is_applicable(self, hass: HomeAssistant) -> bool:
        # Always applicable: harmless global option.
        return True

    async def build_schema(self, hass: HomeAssistant, current: int):
        # `current` may be missing or an int; default to 0 to preserve
        # existing behaviour for upgrades.
        current_value = int(current or 0)
        number = NumberSelector(
            NumberSelectorConfig(
                min=_MIN,
                max=_MAX,
                step=_STEP,
                mode=NumberSelectorMode.BOX,
                unit_of_measurement="%",
            )
        )
        return vol.Schema(
            {
                vol.Required(
                    "tilt_tolerance",
                    description={"suggested_value": current_value},
                    default=current_value,
                ): number
            }
        )

    async def transform_user_input(self, hass: HomeAssistant, user_input: dict[str, int]) -> int:
        # Persist as a single int rather than a mapping
        try:
            val = int(float(user_input.get("tilt_tolerance", 0)))
        except (TypeError, ValueError):
            val = 0
        return max(_MIN, min(_MAX, val))
