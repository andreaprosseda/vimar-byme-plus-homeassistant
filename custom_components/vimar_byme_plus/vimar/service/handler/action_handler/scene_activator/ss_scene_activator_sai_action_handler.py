from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_alarm import VimarAlarm
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler


class SsSceneActivatorSaiActionHandler(BaseActionHandler):
    """Action handler for SS_SceneActivator_Sai as alarm_control_panel."""

    SSTYPE = SsType.SCENE_ACTIVATOR_SAI.value

    ACTION_TO_SFE = {
        ActionType.ALARM_DISARM: SfeType.CMD_AREA_DIS_ACTIVE_SCENE,
        ActionType.ALARM_ARM_AWAY: SfeType.CMD_AREA_ON_ACTIVE_SCENE,
        ActionType.ALARM_ARM_HOME: SfeType.CMD_AREA_INT_ACTIVE_SCENE,
        ActionType.ALARM_ARM_NIGHT: SfeType.CMD_AREA_PAR_ACTIVE_SCENE,
        ActionType.ALARM_TRIGGER: SfeType.CMD_AREA_ALARM_ACTIVE_SCENE,
    }

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if not isinstance(component, VimarAlarm):
            raise NotImplementedError
        sfetype = self.ACTION_TO_SFE.get(action_type)
        if not sfetype:
            raise NotImplementedError(f"Alarm action not supported: {action_type}")
        return [self._action(component.id, sfetype, "Execute")]
