from enum import Enum
from typing import Optional

class IntegrationPhase(Enum):
    SESSION = 'session'
    ATTACH = 'attach'
    AMBIENT_DISCOVERY = 'ambientdiscovery'
    SF_DISCOVERY = 'sfdiscovery'
    REGISTER = 'register'
    CHANGE_STATUS = 'changestatus'
    EXPIRE = 'expire'
    KEEP_ALIVE = 'keepalive'
    DETACH = 'detach'
    
    @staticmethod
    def get(function: str) -> Optional['IntegrationPhase']:
        for elem in IntegrationPhase:
            if elem.value == function:
                return elem
        return None