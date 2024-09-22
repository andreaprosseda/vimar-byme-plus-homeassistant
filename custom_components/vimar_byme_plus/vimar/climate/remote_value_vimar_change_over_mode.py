"""
Module for managing an 1 count remote value.

DPT 6.010.
"""

from __future__ import annotations

import logging

from xknx.dpt import DPTArray, DPTBinary, DPTValue1Count
from xknx.remote_value import RemoteValue

from ..enum.change_over_mode import ChangeOverMode

_LOGGER = logging.getLogger(__name__)


class RemoteValueVimarChangeOverMode(RemoteValue[ChangeOverMode]):
    """Abstraction for remote value of KNX 6.010 (DPT_Value_1_Count)."""

    def to_knx(self, value: ChangeOverMode) -> DPTArray:
        """Convert value to payload."""
        return DPTValue1Count.to_knx(value.value)

    def from_knx(self, payload: DPTArray | DPTBinary) -> ChangeOverMode:
        """Convert current payload to value."""
        _LOGGER.info(payload)
        _LOGGER.info(payload.value)

        return DPTValue1Count.from_knx(payload)
