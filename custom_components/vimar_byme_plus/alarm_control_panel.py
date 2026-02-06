"""Platform for alarm control panel integration (SS_SceneActivator_Sai)."""

from __future__ import annotations

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_alarm import VimarAlarm
from .vimar.model.enum.action_type import ActionType
from .vimar.utils.logger import log_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up alarm control panels from a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_alarm_control_panels()
    entities = [AlarmControlPanel(coordinator, comp) for comp in components]
    log_info(__name__, f"Alarm control panels found: {len(entities)}")
    async_add_entities(entities, True)


class AlarmControlPanel(BaseEntity, AlarmControlPanelEntity):
    """Vimar SAI alarm panel as Home Assistant alarm_control_panel."""

    _component: VimarAlarm

    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_AWAY
        | AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.ARM_NIGHT
        | AlarmControlPanelEntityFeature.TRIGGER
    )
    _attr_code_arm_required = False

    def __init__(self, coordinator: Coordinator, component: VimarAlarm) -> None:
        """Initialize the alarm control panel."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def alarm_state(self) -> AlarmControlPanelState | None:
        """Return the current alarm state."""
        return AlarmControlPanelState.DISARMED

    def alarm_disarm(self, code: str | None = None) -> None:
        """Send disarm command (AreaDis)."""
        self.send(ActionType.ALARM_DISARM)

    def alarm_arm_away(self, code: str | None = None) -> None:
        """Send arm away command (AreaOn - Inserimento)."""
        self.send(ActionType.ALARM_ARM_AWAY)

    def alarm_arm_home(self, code: str | None = None) -> None:
        """Send arm home command (AreaInt - Interno)."""
        self.send(ActionType.ALARM_ARM_HOME)

    def alarm_arm_night(self, code: str | None = None) -> None:
        """Send arm night command (AreaPar - Parziale)."""
        self.send(ActionType.ALARM_ARM_NIGHT)

    def alarm_trigger(self, code: str | None = None) -> None:
        """Send alarm trigger command (AreaAlarm)."""
        self.send(ActionType.ALARM_TRIGGER)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle device update."""
        super()._handle_coordinator_update()
