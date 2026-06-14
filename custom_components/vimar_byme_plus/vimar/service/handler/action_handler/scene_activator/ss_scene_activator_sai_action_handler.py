from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_button import VimarButton
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_scene_activator_activator_action_handler import (
    SsSceneActivatorActivatorActionHandler,
)

# Mapping suffisso button-id → Cmd Vimar. Le chiavi devono coincidere con
# i suffissi usati in SsSceneActivatorSaiMapper.
_SUFFIX_TO_CMD: dict[str, SfeType] = {
    "dis": SfeType.CMD_AREA_DIS_ACTIVE_SCENE,
    "on": SfeType.CMD_AREA_ON_ACTIVE_SCENE,
    "int": SfeType.CMD_AREA_INT_ACTIVE_SCENE,
    "par": SfeType.CMD_AREA_PAR_ACTIVE_SCENE,
    "alarm": SfeType.CMD_AREA_ALARM_ACTIVE_SCENE,
    "alarm_memory": SfeType.CMD_AREA_ALARM_MEMORY_ACTIVE_SCENE,
    "alarm_memory_reset": SfeType.CMD_AREA_ALARM_MEMORY_RESET_ACTIVE_SCENE,
    "alarm_reset": SfeType.CMD_AREA_ALARM_RESET_ACTIVE_SCENE,
}


class SsSceneActivatorSaiActionHandler(SsSceneActivatorActivatorActionHandler):
    SSTYPE = SsType.SCENE_ACTIVATOR_SAI.value
    _SUFFIX_TO_CMD = _SUFFIX_TO_CMD

    def get_press_actions(self, component: VimarButton) -> list[VimarAction]:
        suffix = self._extract_suffix(component.id)
        cmd = self._SUFFIX_TO_CMD.get(suffix)
        if cmd is None:
            raise NotImplementedError
        return [self._action(component.id, cmd, "Execute")]

    @staticmethod
    def _extract_suffix(button_id: str) -> str:
        # button_id has the shape "<idsf>_<suffix>" — split on the first
        # underscore so multi-word suffixes (e.g. "alarm_memory_reset")
        # survive intact.
        if "_" not in str(button_id):
            return ""
        return str(button_id).split("_", 1)[1]
