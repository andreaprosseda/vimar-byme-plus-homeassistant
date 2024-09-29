from typing import Optional
from .communication import Communication
from .credential import Credential
from .client_info import ClientInfo
from dataclasses import dataclass, field

@dataclass
class Parameter:
    idambient: list = field(default_factory=list)
    
    def __init__(self, ambient_ids: list[int] = []):
        self.idambient = ambient_ids