"""Implementation of different VIMAR HVAC Operation modes."""

from __future__ import annotations

import logging

from enum import Enum
from typing import Generic, TypeVar

from xknx.dpt import DPTBase
from xknx.dpt.payload import DPTArray, DPTBinary
from xknx.exceptions import ConversionError

HVACModeT = TypeVar("HVACModeT", "HVACControllerMode", "HVACOperationMode")

_LOGGER = logging.getLogger(__name__)


# ruff: noqa: RUF012  # Mutable class attributes should be annotated with `typing.ClassVar`
class HVACOperationMode(Enum):
    """Enum for the different VIMAR HVAC operation modes."""

    AUTO = "Auto"
    COMFORT = "Comfort"
    STANDBY = "Standby"
    NIGHT = "Night"
    FROST_PROTECTION = "Frost Protection"
    OFF = "Off"


class HVACControllerMode(Enum):
    """Enum for the different VIMAR HVAC controller modes."""

    HEAT = "Heat"
    COOL = "Cool"


class _DPTClimateMode(DPTBase, Generic[HVACModeT]):
    """Base class for KNX Climate modes."""

    SUPPORTED_MODES: dict[int, HVACModeT] = {}

    payload_type = DPTArray
    payload_length = 1

    @classmethod
    def from_knx(cls, payload: DPTArray | DPTBinary) -> HVACModeT:
        """Parse/deserialize from KNX/IP raw data."""
        _LOGGER.info("ClimateMode FROM_KNX payload %s", payload)
        raw = cls.validate_payload(payload)
        _LOGGER.info("ClimateMode FROM_KNX raw %s", raw)
        try:
            return cls.SUPPORTED_MODES[raw[0]]
        except KeyError:
            raise ConversionError(
                f"Payload not supported for {cls.__name__}", raw=raw
            ) from None

    @classmethod
    def to_knx(cls, value: HVACModeT) -> DPTArray:
        """Serialize to KNX/IP raw data."""
        for knx_value, mode in cls.SUPPORTED_MODES.items():
            if mode == value:
                return DPTArray(knx_value)
        raise ConversionError(f"Value not supported for {cls.__name__}", value=value)


class DPTHVACContrMode(_DPTClimateMode[HVACControllerMode]):
    """Abstraction for VIMAR ChangeOverMode."""

    SUPPORTED_MODES: dict[int, HVACControllerMode] = {
        1: HVACControllerMode.COOL,
        2: HVACControllerMode.HEAT,
    }


class DPTHVACMode(_DPTClimateMode[HVACOperationMode]):
    """Abstraction for VIMAR HVAC mode."""

    SUPPORTED_MODES: dict[int, HVACOperationMode] = {
        0: HVACOperationMode.AUTO,
        1: HVACOperationMode.COMFORT,
        2: HVACOperationMode.STANDBY,
        3: HVACOperationMode.NIGHT,
        4: HVACOperationMode.FROST_PROTECTION,
        5: HVACOperationMode.OFF,
        6: HVACOperationMode.OFF,
    }


class DPTControllerStatus(_DPTClimateMode[HVACOperationMode]):
    """Abstraction for VIMAR HVAC Controller status."""

    SUPPORTED_MODES: dict[int, HVACOperationMode] = {
        0x21: HVACOperationMode.COMFORT,
        0x22: HVACOperationMode.STANDBY,
        0x24: HVACOperationMode.NIGHT,
        0x28: HVACOperationMode.FROST_PROTECTION,
    }

    @classmethod
    def from_knx(cls, payload: DPTArray | DPTBinary) -> HVACOperationMode:
        """Parse/deserialize from KNX/IP raw data."""
        _LOGGER.info("ControllerStatus FROM_KNX payload %s", payload)
        raw = cls.validate_payload(payload)
        _LOGGER.info("FROM_KNX %s", raw[0])
        if raw[0] & 8 > 0:
            return HVACOperationMode.OFF
        if raw[0] & 8 > 0:
            return HVACOperationMode.FROST_PROTECTION
        if raw[0] & 4 > 0:
            return HVACOperationMode.NIGHT
        if raw[0] & 2 > 0:
            return HVACOperationMode.STANDBY
        if raw[0] & 1 > 0:
            return HVACOperationMode.COMFORT
        raise ConversionError(f"Payload not supported for {cls.__name__}", raw=raw)
