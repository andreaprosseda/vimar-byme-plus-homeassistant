"""OptionsFlow section: per-device kind for SS_Energy_MeasureCounter.

Lets the user pick electricity / water / gas for each Vimar pulse
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

    def __init__(self) -> None:
        # Cached on build_schema, consumed in transform_user_input to
        # convert from human-readable form labels back to idsf-keyed
        # storage.
        self._counters: list[tuple[int, str]] = []

    async def is_applicable(self, hass: HomeAssistant) -> bool:
        counters = await hass.async_add_executor_job(self._get_counters)
        return bool(counters)

    async def build_schema(
        self, hass: HomeAssistant, current: dict[str, Any]
    ) -> vol.Schema:
        counters = await hass.async_add_executor_job(self._get_counters)
        self._counters = counters
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
                    self._label(idsf, name),
                    description={
                        "suggested_value": current.get(
                            str(idsf), COUNTER_ELECTRICITY
                        )
                    },
                    default=COUNTER_ELECTRICITY,
                ): select
                for idsf, name in counters
            }
        )

    async def description_placeholders(
        self, hass: HomeAssistant
    ) -> dict[str, str]:
        counters = await hass.async_add_executor_job(self._get_counters)
        return {"count": str(len(counters))}

    async def transform_user_input(
        self, hass: HomeAssistant, user_input: dict[str, Any]
    ) -> dict[str, str]:
        counters = self._counters or await hass.async_add_executor_job(
            self._get_counters
        )
        label_to_idsf = {self._label(idsf, name): str(idsf) for idsf, name in counters}
        out: dict[str, str] = {}
        for label, value in user_input.items():
            idsf_key = label_to_idsf.get(label)
            if idsf_key is None:
                continue
            out[idsf_key] = value
        return out

    @staticmethod
    def _label(idsf: int, name: str) -> str:
        # Disambiguate by appending the device idsf, in case two Vimar
        # devices share the same friendly name.
        return f"{name} (#{idsf})"

    @staticmethod
    def _get_counters() -> list[tuple[int, str]]:
        try:
            components = Database.instance().component_repo.get_all()
        except Exception:  # pylint: disable=broad-except
            return []
        sstype = SsType.ENERGY_MEASURE_COUNTER.value
        return [(c.idsf, c.name) for c in components if c.sstype == sstype]
