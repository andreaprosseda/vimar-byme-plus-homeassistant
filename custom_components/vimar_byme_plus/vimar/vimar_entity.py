"""Insteon base entity."""

import logging

from xknx.devices import Device

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinator import VimarDataUpdateCoordinator
from ..utils.ip_to_knx import get_knx_group_address
from .model.byme_configuration.application import Application
from .model.byme_configuration.environment import Environment
from .model.byme_configuration.group_address import GroupAddress
from .model.vimar_addresses import VimarAddresses
from .model.vimar_application import VimarApplication, VimarType

_LOGGER = logging.getLogger(__name__)


class VimarEntity(CoordinatorEntity):
    """Vimar abstract base entity."""

    _device: Device
    _type: VimarType
    _app: Application
    _env: Environment

    def __init__(
        self,
        coordinator: VimarDataUpdateCoordinator,
        app: VimarApplication,
        device: Device,
    ) -> None:
        """Initialize VimarEntity."""
        super().__init__(coordinator)
        self._type = app.type
        self._app = app.application
        self._env = app.environment
        self._device = device

    @property
    def device_name(self):
        """Return the name of the device."""
        return self._app.label

    @property
    def name(self):
        """Return the name of the device."""
        return self.device_name

    # @property
    # def extra_state_attributes(self):

    # @property
    # def icon(self):

    @property
    def device_class(self):
        """Return type of the device."""
        return self._type.value.get("device_class")

    @property
    def unique_id(self):
        """Return unique id of the device."""
        return DOMAIN + "_app_" + self._app.id

    @property
    def is_default_state(self):
        """Return True of in default state - resulting in default icon."""
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._app.id)},
            manufacturer="Vimar",
            name=self._app.label,
            model=self._app.channel,
            suggested_area=self._env.label,
        )

    async def async_update(self) -> None:
        """Request a state update from KNX bus."""
        await self._device.sync()

    async def after_update_callback(self, device: Device) -> None:
        """Call after device was updated."""
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Store register state change callback."""
        await super().async_added_to_hass()
        self._device.register_device_updated_cb(self.after_update_callback)
        # will remove all callbacks and xknx tasks
        self.async_on_remove(self._device.shutdown)

    def _get_addresses(self, app: Application) -> VimarAddresses:
        return VimarAddresses(
            hvac_mode=self._get_address(app, "DPTx_HvacMode"),
            hvac_mode_info=self._get_address(app, "DPTx_HvacModeInfo"),
            change_over_mode=self._get_address(app, "DPTx_ChangeOverMode"),
            change_over_mode_info=self._get_address(app, "DPTx_ChangeOverModeInfo"),
            ambient_temperature=self._get_address(app, "DPTx_AmbientTemperature"),
            temperature_setpoint=self._get_address(app, "DPTx_TemperatureSetpoint1"),
            temperature_setpoint_info=self._get_address(
                app, "DPTx_TemperatureSetpointInfo1"
            ),
        )

    def _get_address(self, key: str) -> str | None:
        return self._get_address(self._app, key)

    def _get_address(self, app: Application, key: str) -> str | None:
        group = app.groups[0]
        addresses = group.group_addresses
        group_address = next(filter(lambda x: self._same_key(x, key), addresses), None)
        return get_knx_group_address(group_address.address)

    def _same_key(self, address: GroupAddress, key: str) -> bool:
        if address.dpt.name == key:  # .value:
            return True
        if address.dptx.name == key:  # .value:
            return True
        return False
