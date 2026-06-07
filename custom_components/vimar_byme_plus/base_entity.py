"""Insteon base entity."""

from websocket import WebSocketConnectionClosedException

from homeassistant.core import HomeAssistantError, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANIFACTURER
from .coordinator import Coordinator
from .vimar.model.component.vimar_component import VimarComponent
from .vimar.model.enum.action_type import ActionType
from .vimar.model.exceptions import VimarErrorResponseException
from .vimar.model.gateway.vimar_data import VimarData


class BaseEntity(CoordinatorEntity):
    """Vimar abstract base entity."""

    _component: VimarComponent

    def __init__(self, coordinator: Coordinator, component: VimarComponent) -> None:
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
        return self._component.device_class

    @property
    def unique_id(self):
        """Return unique id of the device, scoped per gateway.

        With per-gateway databases (PR #72) each gateway's `idsf` space is
        independent, so `idsf` is NOT globally unique across gateways: e.g.
        idsf 1003 is "Applique ingresso" on one gateway and "luce cucina"
        on another. The previous `vimar_byme_plus_app_<idsf>` therefore
        produced identical unique_ids for two different entities on two
        gateways; Home Assistant keeps only the first and silently drops the
        second ("Platform vimar_byme_plus does not generate unique IDs").
        Including the gateway deviceuid makes them distinct. Single-gateway
        installs are migrated by `async_migrate_entry` so existing entity
        customisations are preserved (see __init__.py).
        """
        gw_uid = getattr(self.coordinator, "gateway_info", None)
        if gw_uid is not None:
            gw_uid = getattr(gw_uid, "deviceuid", None)
        if gw_uid:
            return f"{DOMAIN}_{gw_uid}_app_{self._component.id}"
        return f"{DOMAIN}_app_{self._component.id}"

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

    def send(self, actionType: ActionType, *args) -> None:
        """Send a request coming from HomeAssistant to Gateway."""
        try:
            component = self._component
            coordinator: Coordinator = self.coordinator
            coordinator.send(component, actionType, *args)
        except WebSocketConnectionClosedException as err:
            message = "Connection with Gateway is closed, restart the integration"
            raise HomeAssistantError(message) from err
        except NotImplementedError as err:
            message = "Method not implemented, contact the creator on GitHub"
            raise HomeAssistantError(message) from err
        except VimarErrorResponseException as err:
            message = f"Error received from Gateway: {err.message}"
            raise HomeAssistantError(message) from err

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state. False if entity pushes its state to HA."""
        return False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle device update."""
        if self._component:
            data: VimarData = self.coordinator.data
            self._component = data.get_by_id(self._component.id)
            self.async_write_ha_state()
