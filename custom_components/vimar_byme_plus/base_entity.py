"""Insteon base entity."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANIFACTURER
from .coordinator import VimarDataUpdateCoordinator
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.component_type import ComponentType

class BaseEntity(CoordinatorEntity):
    """Vimar abstract base entity."""

    _component: VimarComponent

    def __init__(
        self,
        coordinator: VimarDataUpdateCoordinator,
        component: VimarComponent,
    ) -> None:
        """Initialize BaseEntity."""
        super().__init__(coordinator)
        self._component = component

    @property
    def device_name(self):
        """Return the name of the device."""
        return self._component.device_name

    @property
    def name(self):
        """Return the name of the device."""
        return self._component.name

    @property
    def icon(self):

    @property
    def device_class(self):
        """Return type of the device."""
        name = self._component.device_name
        return ComponentType.from_type(name).device_class()

    @property
    def unique_id(self):
        """Return unique id of the device."""
        return DOMAIN + "_app_" + str(self._component.id)

    @property
    def is_default_state(self):
        """Return True if in default state - resulting in default icon."""
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._component.id)},
            manufacturer=MANIFACTURER,
            name=self._component.name,
            model=self._component.device_name,
            suggested_area=self._component.area,
        )

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
