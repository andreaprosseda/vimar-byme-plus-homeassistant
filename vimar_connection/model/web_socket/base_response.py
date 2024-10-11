from dataclasses import dataclass, asdict, field
from ...utils.json import json_dumps
from ...utils.mac_address import get_mac_address

@dataclass
class BaseResponse:
    type: str
    function: str
    source: str
    target: str
    token: str
    msgid: str
    error: int
    result: list = field(default_factory=list)

    def __init__(self):
        self.type = 'response'
        self.source = get_mac_address()
        self.error = 0
        self.result = []
        
    def to_json(self):
        return json_dumps(asdict(self))
