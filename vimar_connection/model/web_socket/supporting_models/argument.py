from typing import Optional
from .communication import Communication
from .credential import Credential
from .client_info import ClientInfo
from dataclasses import dataclass

@dataclass
class Argument:
    credential: Optional[Credential]
    clientinfo: Optional[ClientInfo]
    communication: Optional[Communication]
    user: Optional[str] # logout / remove
    sfcategory: Optional[str]
    
    def __init__(self, 
                 communication: Communication = None, 
                 credential: Credential = None, 
                 clientinfo: ClientInfo = None, 
                 user: str = None,
                 sfcategory: str = None
        ):
        self.communication = communication
        self.credential = credential
        self.clientinfo = clientinfo
        self.user = user
        self.sfcategory = sfcategory