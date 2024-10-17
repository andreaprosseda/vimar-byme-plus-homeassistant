"""Insteon base entity."""

import logging

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinator import VimarDataUpdateCoordinator
from ..vimar.database.database import Database
from ..vimar.model.enum.component_type import ComponentType
from ..vimar.model.repository.user_component import UserComponent

_LOGGER = logging.getLogger(__name__)


class VimarEntity(CoordinatorEntity):
    """Vimar abstract base entity."""

    _component: UserComponent
    _ambient_repo = Database.instance().ambient_repo
    _element_repo = Database.instance().element_repo

    def __init__(
        self,
        coordinator: VimarDataUpdateCoordinator,
        component: UserComponent,
    ) -> None:
        """Initialize VimarEntity."""
        super().__init__(coordinator)
        self._component = component

    @property
    def device_name(self):
        """Return the name of the device."""
        return self._component.sftype

    @property
    def name(self):
        """Return the name of the device."""
        return self._component.name

    # @property
    # def extra_state_attributes(self):

    # @property
    # def icon(self):

    @property
    def device_class(self):
        """Return type of the device."""
        sftype = self._component.sftype
        return ComponentType.from_type(sftype).device_class()

    @property
    def unique_id(self):
        """Return unique id of the device."""
        return DOMAIN + "_app_" + str(self._component.idsf)

    @property
    def is_default_state(self):
        """Return True if in default state - resulting in default icon."""
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        area = self.get_ambient_name_from_id(self._component.idambient)
        return DeviceInfo(
            identifiers={(DOMAIN, self._component.idsf)},
            manufacturer="Vimar",
            name=self._component.name,
            model=self._component.sftype,
            suggested_area=area,
        )

    def get_ambient_name_from_id(self, idambient: int) -> str:
        """Return ambient name from ambient id."""
        return self._ambient_repo.get_name_by_id(idambient)

    def get_element(self, type: str) -> str:
        """Return element value name from ambient id."""
        idelement = self._component.idsf
        return self._element_repo.get_value_by_id(idelement, type)

    # async def async_update(self) -> None:
    #     """Request a state update from KNX bus."""
    #     await self._device.sync()

    # async def after_update_callback(self, device: Device) -> None:
    #     """Call after device was updated."""
    #     self.async_write_ha_state()

    # async def async_added_to_hass(self) -> None:
    #     """Store register state change callback."""
    #     await super().async_added_to_hass()
    #     self._device.register_device_updated_cb(self.after_update_callback)
    #     # will remove all callbacks and xknx tasks
    #     self.async_on_remove(self._device.shutdown)
