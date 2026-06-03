"""OptionsFlow section: per-device auto-press of "Aggiornamenti RealTime"."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from ..const import SECTION_REALTIME
from .base import OptionsSection
from ..vimar.model.gateway.vimar_data import VimarData
from ..vimar.model.component.vimar_button import VimarButton

_REALTIME_BUTTON_MARKER = "real_time"
_MIN_INTERVAL = 0
_MAX_INTERVAL = 3600
_STEP = 1


class RealtimeSection(OptionsSection):
    """Auto-press interval picker per real-time button."""

    id = SECTION_REALTIME

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        # Cached on build_schema, consumed in transform_user_input to
        # convert from human-readable form keys back to the canonical
        # idsf-keyed storage map.
        self._buttons: list[VimarButton] = []

    async def is_applicable(self, hass: HomeAssistant) -> bool:
        return bool(self._collect_buttons())

    async def build_schema(
        self, hass: HomeAssistant, current: dict[str, Any]
    ) -> vol.Schema:
        buttons = self._collect_buttons()
        self._buttons = buttons
        number = NumberSelector(
            NumberSelectorConfig(
                min=_MIN_INTERVAL,
                max=_MAX_INTERVAL,
                step=_STEP,
                mode=NumberSelectorMode.BOX,
                unit_of_measurement="s",
            )
        )
        schema_dict: dict[Any, Any] = {}
        for button in buttons:
            label = self._label(button)
            current_value = self._coerce_int(
                current.get(str(button.main_id), 0)
            )
            schema_dict[
                vol.Required(
                    label,
                    description={"suggested_value": current_value},
                    default=0,
                )
            ] = number
        return vol.Schema(schema_dict)

    async def description_placeholders(
        self, hass: HomeAssistant
    ) -> dict[str, str]:
        buttons = self._collect_buttons()
        return {
            "count": str(len(buttons)),
            "max_seconds": str(_MAX_INTERVAL),
        }

    async def transform_user_input(
        self, hass: HomeAssistant, user_input: dict[str, Any]
    ) -> dict[str, int]:
        buttons = self._buttons or self._collect_buttons()
        label_to_main_id = {self._label(b): str(b.main_id) for b in buttons}
        out: dict[str, int] = {}
        for label, value in user_input.items():
            main_id = label_to_main_id.get(label)
            if main_id is None:
                continue
            out[main_id] = self._coerce_int(value)
        return out

    @staticmethod
    def _label(button: VimarButton) -> str:
        return f"{button.name} (#{button.main_id})"

    @staticmethod
    def _coerce_int(value: Any) -> int:
        try:
            return max(_MIN_INTERVAL, min(_MAX_INTERVAL, int(float(value))))
        except (TypeError, ValueError):
            return 0

    def _collect_buttons(self) -> list[VimarButton]:
        try:
            coordinator = self._entry.runtime_data
            data: VimarData = coordinator.data
            buttons: list[VimarButton] = data.get_buttons()
            return [b for b in buttons if _REALTIME_BUTTON_MARKER in str(b.id)]
        except Exception:  # pylint: disable=broad-except
            return []