"""Insteon base entity."""

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANIFACTURER
from .coordinator import Coordinator
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.component_type import ComponentType
from .vimar.model.gateway.vimar_data import VimarData
from .vimar.model.enum.action_type import ActionType


class BaseEntity(CoordinatorEntity):
    """Vimar abstract base entity."""

    _component: VimarComponent

    def __init__(
        self,
        coordinator: Coordinator,
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

    # @property
    # def icon(self):

    @property
    def device_class(self):
        """Return type of the device."""
        name = self._component.device_group
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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle device update."""
        data: VimarData = self.coordinator.data
        self._component = data.get_by_id(self._component.id)
        self.async_write_ha_state()

    def send(self, actionType: ActionType, *args) -> None:
        """Send a request coming from HomeAssistant to Gateway."""
        component = self._component
        coordinator: Coordinator = self.coordinator
        coordinator.send(component, actionType, *args)
