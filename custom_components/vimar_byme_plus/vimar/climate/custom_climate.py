"""Custom implementation of XKNX climate.py"""

from __future__ import annotations

from collections.abc import Iterator
import logging
from typing import TYPE_CHECKING, Any

from xknx.devices.device import Device, DeviceCallbackType
from xknx.remote_value import GroupAddressesType, RemoteValue, RemoteValueTemp

from .custom_climate_mode import CustomClimateMode, HVACOperationMode

if TYPE_CHECKING:
    from xknx.telegram import Telegram
    from xknx.telegram.address import DeviceGroupAddress
    from xknx.xknx import XKNX

_LOGGER = logging.getLogger(__name__)

DEFAULT_TEMPERATURE_STEP = 0.1


class CustomClimate(Device):
    """Class for managing the climate."""

    def __init__(
        self,
        xknx: XKNX,
        name: str,
        group_address_temperature: GroupAddressesType = None,
        group_address_target_temperature: GroupAddressesType = None,
        group_address_target_temperature_state: GroupAddressesType = None,
        sync_state: bool | float | str = True,
        min_temp: float | None = None,
        max_temp: float | None = None,
        mode: CustomClimateMode | None = None,
        device_updated_cb: DeviceCallbackType[CustomClimate] | None = None,
    ) -> None:
        """Initialize Climate class."""
        super().__init__(xknx, name, device_updated_cb)

        self.min_temp = min_temp
        self.max_temp = max_temp
        self.temperature_step = DEFAULT_TEMPERATURE_STEP
        self.mode = mode

        self.temperature = RemoteValueTemp(
            xknx,
            group_address_state=group_address_temperature,
            sync_state=sync_state,
            device_name=self.name,
            feature_name="Current temperature",
            after_update_cb=self.after_update,
        )

        self.target_temperature = RemoteValueTemp(
            xknx,
            group_address_target_temperature,
            group_address_target_temperature_state,
            sync_state=sync_state,
            device_name=self.name,
            feature_name="Target temperature",
            after_update_cb=self.after_update,
        )

    def _iter_remote_values(self) -> Iterator[RemoteValue[Any]]:
        """Iterate the devices RemoteValue classes."""
        yield self.temperature
        yield self.target_temperature

    def has_group_address(self, group_address: DeviceGroupAddress) -> bool:
        """Test if device has given group address."""
        if self.mode is not None and self.mode.has_group_address(group_address):
            return True
        return super().has_group_address(group_address)

    def is_on(self) -> bool:
        """Return power status."""
        return self.mode.operation_mode != HVACOperationMode.OFF

    @property
    def is_active(self) -> bool | None:
        """Return if currently active. None if unknown."""
        return self.mode.operation_mode != HVACOperationMode.OFF

    async def turn_on(self) -> None:
        """Set power status to on."""
        raise NotImplementedError

    async def turn_off(self) -> None:
        """Set power status to off."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Shutdown this device and the underlying mode."""
        super().shutdown()
        if self.mode:
            self.mode.shutdown()

    @property
    def initialized_for_setpoint_shift_calculations(self) -> bool:
        """Test if object is initialized for setpoint shift calculations."""
        return False

    async def set_target_temperature(self, target_temperature: float) -> None:
        """Send new target temperature or setpoint_shift to KNX bus."""
        validated_temp = self.validate_value(
            target_temperature, self.min_temp, self.max_temp
        )
        await self.target_temperature.set(validated_temp)

    @property
    def base_temperature(self) -> float | None:
        """Return the base temperature when setpoint_shift is initialized."""
        return None

    @property
    def setpoint_shift(self) -> float | None:
        """Return current offset from base temperature in Kelvin."""
        return None

    def validate_value(
        self, value: float, min_value: float | None, max_value: float | None
    ) -> float:
        """Check boundaries of temperature and return valid temperature value."""
        if (min_value is not None) and (value < min_value):
            _LOGGER.warning("Min value exceeded at %s: %s", self.name, value)
            return min_value
        if (max_value is not None) and (value > max_value):
            _LOGGER.warning("Max value exceeded at %s: %s", self.name, value)
            return max_value
        return value

    @property
    def target_temperature_max(self) -> float | None:
        """Return the highest possible target temperature."""
        if self.max_temp is not None:
            return self.max_temp
        return None

    @property
    def target_temperature_min(self) -> float | None:
        """Return the lowest possible target temperature."""
        if self.min_temp is not None:
            return self.min_temp
        return None

    async def process_group_write(self, telegram: Telegram) -> None:
        """Process incoming and outgoing GROUP WRITE telegram."""
        for remote_value in self._iter_remote_values():
            await remote_value.process(telegram)
        if self.mode is not None:
            await self.mode.process_group_write(telegram)

    async def sync(self, wait_for_result: bool = False) -> None:
        """Read states of device from KNX bus."""
        await super().sync(wait_for_result=wait_for_result)
        if self.mode is not None:
            await self.mode.sync(wait_for_result=wait_for_result)

    def __str__(self) -> str:
        """Return object as readable string."""
        return (
            f'<Climate name="{self.name}" '
            f"temperature={self.temperature.group_addr_str()} "
            f"target_temperature={self.target_temperature.group_addr_str()} "
            f'temperature_step="{self.temperature_step}" '
            f'setpoint_shift_max="{self.setpoint_shift_max}" '
            f'setpoint_shift_min="{self.setpoint_shift_min}" '
            "/>"
        )
