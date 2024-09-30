from typing import Optional
from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class UserCredentials:
    username: Optional[str]
    setup_code: Optional[str]
    useruid: Optional[str]
    password: Optional[str]
    token: Optional[str]
    
    def __init__(self, username: str = None, useruid: str = None, password: str = None, setup_code: str = None, token: str = None):
        self.username = username
        self.setup_code = setup_code
        self.useruid = useruid
        self.password = password
        self.token = token
        
    def to_json(self):
        return json_dumps(asdict(self))
