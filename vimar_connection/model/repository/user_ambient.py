from typing import Optional
from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class UserAmbient:
    dictKey: Optional[str]
    hash: Optional[str]
    idambient: Optional[int]
    idparent: Optional[int]
    name: Optional[str]
            
    def to_json(self):
        return json_dumps(asdict(self))
    
    def to_tuple(self) -> tuple:
        return (
            self.dictKey, 
            self.hash, 
            self.idambient,
            self.idparent,
            self.name
        )
        
    @staticmethod
    def list_from_dict(response: dict) -> list['UserAmbient']:
        ambients = []
        for result in response['result']:
            ambients.append(UserAmbient(**result))
        return ambients