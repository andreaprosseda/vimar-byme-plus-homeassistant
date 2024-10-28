from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class OperationalRequest:
    username: str
    userid: str
    password: str
    
    def to_dict(self):
        return asdict(self)
    
    def to_json(self):
        return json_dumps(asdict(self))