from typing import Optional
from .communication import Communication
from .credential import Credential
from .client_info import ClientInfo
from dataclasses import dataclass, field

@dataclass
class Argument:
    credential: Optional[Credential]
    clientinfo: Optional[ClientInfo]
    communication: Optional[Communication]
    user: Optional[str] # logout / remove
    sfcategory: Optional[str]
    idsf: Optional[int]
    sfetype: list[str] = field(default_factory=list)
    
    def __init__(self, 
                 communication: Communication = None, 
                 credential: Credential = None, 
                 clientinfo: ClientInfo = None, 
                 user: str = None,
                 sfcategory: str = None,
                 idsf: int = None,
                 sfetype: list[str] = None
        ):
        self.communication = communication
        self.credential = credential
        self.clientinfo = clientinfo
        self.user = user
        self.sfcategory = sfcategory
        self.idsf = idsf
        self.sfetype = sfetype