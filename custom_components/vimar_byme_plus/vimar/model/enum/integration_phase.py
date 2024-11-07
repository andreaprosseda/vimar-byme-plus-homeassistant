from enum import Enum
from typing import Optional


class IntegrationPhase(Enum):
    INIT = "init"
    SESSION = "session"
    ATTACH = "attach"
    AMBIENT_DISCOVERY = "ambientdiscovery"
    SF_DISCOVERY = "sfdiscovery"
    REGISTER = "register"
    CHANGE_STATUS = "changestatus"
    EXPIRE = "expire"
    DO_ACTION = "doaction"
    GET_STATUS = "getstatus"
    KEEP_ALIVE = "keepalive"
    DETACH = "detach"

    @staticmethod
    def get(function: str) -> Optional["IntegrationPhase"]:
        if not function:
            return None
        for elem in IntegrationPhase:
            if elem.value == function:
                return elem
        return None
