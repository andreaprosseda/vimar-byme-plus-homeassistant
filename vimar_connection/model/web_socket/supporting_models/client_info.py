from dataclasses import dataclass
from typing import Optional

@dataclass
class ClientInfo:
    clienttag: str
    sfmodelversion: str
    protocolversion: str
    manufacturertag: Optional[str] = None
    
    def __init__(self, client_tag: str, sf_model_version: str, protocol_version: str, manufacturer_tag: Optional[str] = None):
        self.clienttag = client_tag
        self.sfmodelversion = sf_model_version
        self.protocolversion = protocol_version
        self.manufacturertag = manufacturer_tag
