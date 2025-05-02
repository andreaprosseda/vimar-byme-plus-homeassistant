from dataclasses import dataclass

from ..base_request import BaseRequest


@dataclass
class AmbientDiscoveryRequest(BaseRequest):
    def __init__(self, target: str, token: str):
        super().__init__()
        self.function = "ambientdiscovery"
        self.target = target
        self.token = token
        self.msgid = "1"
