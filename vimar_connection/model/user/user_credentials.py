from typing import Optional
from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class UserCredentials:
    setup_code: Optional[str]
    useruid: Optional[str]
    password: Optional[str]
    
    def __init__(self, useruid: str = None, password: str = None, setup_code: str = None):
        self.setup_code = setup_code
        self.useruid = useruid
        self.password = password
        
    def to_json(self):
        return json_dumps(asdict(self))
