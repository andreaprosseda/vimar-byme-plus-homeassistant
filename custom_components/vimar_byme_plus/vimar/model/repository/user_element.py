from typing import Optional
from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class UserElement:
    enable: Optional[bool]
    idcomponent: Optional[int]
    sfetype: Optional[str]
    value: Optional[str]

    def to_json(self):
        return json_dumps(asdict(self))
    
    def to_tuple(self) -> tuple:
        return (
            self.enable,
            self.idcomponent,
            self.sfetype,
            self.value
        )
        
    def to_tuple_for_update(self) -> tuple:
        return (
            self.enable,
            self.value,
            self.idcomponent,
            self.sfetype
        )
    
    @staticmethod    
    def list_from_dict(id_component: int, elems: dict) -> list['UserElement']:
        elements = []
        for elem in elems:
            elem = UserElement._obj_from_dict(id_component, elem)
            elements.append(elem)
        return elements
    
    @staticmethod
    def _obj_from_dict(id_component: str, elem: dict) -> 'UserElement':
        return UserElement(
            enable = elem.get('enable'),
            idcomponent = id_component,
            sfetype = elem.get('sfetype'),
            value = elem.get('value')
        )