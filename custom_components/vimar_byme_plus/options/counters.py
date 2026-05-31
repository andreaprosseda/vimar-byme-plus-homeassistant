"""OptionsFlow section: per-device kind for SS_Energy_MeasureCounter (01452).

Lets the user pick electricity / water / gas for each Vimar 01452 pulse
counter so the integration applies the right device_class / unit /
value scaling.
"""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from ..const import (
    COUNTER_ELECTRICITY,
    COUNTER_GAS,
    COUNTER_WATER,
    SECTION_COUNTERS,
)
from ..vimar.database.database import Database
from ..vimar.model.enum.sstype_enum import SsType
from .base import OptionsSection


class CountersSection(OptionsSection):
    """Counter type picker per pulse-counter device."""

    id = SECTION_COUNTERS

    async def is_applicable(self, hass: HomeAssistant) -> bool:
        counters = await hass.async_add_executor_job(self._get_counters)
        return bool(counters)

    async def build_schema(
        self, hass: HomeAssistant, current: dict[str, Any]
    ) -> vol.Schema:
        counters = await hass.async_add_executor_job(self._get_counters)
        select = SelectSelector(
            SelectSelectorConfig(
                options=[COUNTER_ELECTRICITY, COUNTER_WATER, COUNTER_GAS],
                translation_key="counter_type",
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
        return vol.Schema(
            {
                vol.Required(
                    str(idsf),
                    description={
                        "suggested_value": current.get(
                            str(idsf), COUNTER_ELECTRICITY
                        )
                    },
                    default=COUNTER_ELECTRICITY,
                ): select
                for idsf, _name in counters
            }
        )

    async def description_placeholders(
        self, hass: HomeAssistant
    ) -> dict[str, str]:
        counters = await hass.async_add_executor_job(self._get_counters)
        return {
            "counters": ", ".join(
                f"{name} (#{idsf})" for idsf, name in counters
            )
        }

    @staticmethod
    def _get_counters() -> list[tuple[int, str]]:
        try:
            components = Database.instance().component_repo.get_all()
        except Exception:  # pylint: disable=broad-except
            return []
        sstype = SsType.ENERGY_MEASURE_COUNTER.value
        return [(c.idsf, c.name) for c in components if c.sstype == sstype]
