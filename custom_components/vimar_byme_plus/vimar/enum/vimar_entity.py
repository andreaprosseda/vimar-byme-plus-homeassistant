"""Insteon base entity."""

import logging

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinator import VimarDataUpdateCoordinator
from ..utils.ip_to_knx import get_knx_group_address
from .model.byme_configuration.application import Application
from .model.byme_configuration.environment import Environment
from .model.byme_configuration.group_address import GroupAddress
from .enum.vimar_dpt_values import DptValue
from .model.vimar_application import VimarApplication, VimarType

_LOGGER = logging.getLogger(__name__)


class VimarEntity(CoordinatorEntity):
    """Vimar abstract base entity."""

    type: VimarType
    app: Application
    env: Environment

    def __init__(
        self, coordinator: VimarDataUpdateCoordinator, app: VimarApplication
    ) -> None:
        """Initialize VimarEntity."""
        super().__init__(coordinator)
        self.type = app.type
        self.app = app.application
        self.env = app.environment

    @property
    def device_name(self):
        """Return the name of the device."""
        return self.app.label

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
        return self.type.value.get("device_class")

    @property
    def unique_id(self):
        """Return unique id of the device."""
        return DOMAIN + "_app_" + self.app.id

    @property
    def is_default_state(self):
        """Return True of in default state - resulting in default icon."""
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.app.id)},
            manufacturer="Vimar",
            name=self.app.label,
            model=self.app.channel,
            suggested_area=self.env.label,
        )

    def _get_address(self, key: DptValue) -> str | None:
        group = self.app.groups[0]
        addresses = group.group_addresses
        group_address = next(filter(lambda x: self._same_key(x, key), addresses), None)
        return get_knx_group_address(group_address.address)

    def _same_key(self, address: GroupAddress, key: DptValue) -> bool:
        if address.dpt.name == key.value:
            return True
        if address.dptx.name == key.value:
            return True
        return False
