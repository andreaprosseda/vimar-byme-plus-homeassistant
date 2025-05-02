from dataclasses import dataclass
from enum import Enum


@dataclass
class CommunicationMode(Enum):
    ON_DEMAND_TCP = 1
    ALWAYS_ACTIVE_TCP = 2
    DUAL_MODE_TCP = 3
    WEB_SOCKET = 4


@dataclass
class Communication:
    ipaddress: str
    communicationmode: int | None
    ipport: int | None

    def __init__(self, address: str, port: int = None, mode: CommunicationMode = None):
        self.ipaddress = address
        self.ipport = port
        self.communicationmode = mode.value if mode else None
