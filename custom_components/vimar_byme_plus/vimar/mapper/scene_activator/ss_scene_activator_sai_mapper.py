from ...model.component.vimar_alarm import VimarAlarm
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneActivatorSaiMapper:
    """SS_SceneActivator_Sai: Inserimento allarme (SAI alarm panel).

    Maps to a single Home Assistant alarm_control_panel entity.
    SFEs from Specifiche.out.html: AreaDis, AreaOn, AreaInt, AreaPar,
    AreaAlarm, AreaAlarmMemory, AreaAlarmMemoryReset, AreaAlarmReset.
    """

    SSTYPE = SsType.SCENE_ACTIVATOR_SAI.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarAlarm]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarAlarm:
        return VimarAlarm(
            id=str(component.idsf),
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
        )
