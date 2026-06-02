from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_scene_activator_sai_action_handler import SsSceneActivatorSaiActionHandler

# Mapping suffisso button-id → Cmd Vimar per Saig2. Condivide 5 chiavi
# con Sai (dis/alarm/alarm_memory/alarm_memory_reset/alarm_reset) e ne
# aggiunge 5 specifiche (par_a/b/c/d, total).
_SUFFIX_TO_CMD: dict[str, SfeType] = {
    "dis": SfeType.CMD_AREA_DIS_ACTIVE_SCENE,
    "alarm": SfeType.CMD_AREA_ALARM_ACTIVE_SCENE,
    "alarm_memory": SfeType.CMD_AREA_ALARM_MEMORY_ACTIVE_SCENE,
    "alarm_memory_reset": SfeType.CMD_AREA_ALARM_MEMORY_RESET_ACTIVE_SCENE,
    "alarm_reset": SfeType.CMD_AREA_ALARM_RESET_ACTIVE_SCENE,
    "par_a": SfeType.CMD_AREA_PAR_A_ACTIVE_SCENE,
    "par_b": SfeType.CMD_AREA_PAR_B_ACTIVE_SCENE,
    "par_c": SfeType.CMD_AREA_PAR_C_ACTIVE_SCENE,
    "par_d": SfeType.CMD_AREA_PAR_D_ACTIVE_SCENE,
    "total": SfeType.CMD_AREA_TOTAL_ACTIVE_SCENE,
}


class SsSceneActivatorSaiG2ActionHandler(SsSceneActivatorSaiActionHandler):
    SSTYPE = SsType.SCENE_ACTIVATOR_SAI_G2.value
    _SUFFIX_TO_CMD = _SUFFIX_TO_CMD
