from typing import Optional
from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class UserEnvironment:
    idambient: Optional[int]
    name: Optional[str]
    dictKey: Optional[str]
    hash: Optional[str]
    idparent: Optional[int]
            
    def to_json(self):
        return json_dumps(asdict(self))
