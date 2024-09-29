from dataclasses import dataclass, asdict, field
from ...utils.json import json_dumps
from ...utils.mac_address import get_mac_address

@dataclass
class BaseRequest:
    type: str
    function: str
    source: str
    target: str
    token: str
    msgid: str
    args: list = field(default_factory=list)
    params: list = field(default_factory=list)

    def __init__(self):
        self.type = 'request'
        self.source = get_mac_address()
        self.args = []
        self.params = []
        
    def to_json(self):
        return json_dumps(asdict(self))
