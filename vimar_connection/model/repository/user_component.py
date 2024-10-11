from .user_element import UserElement
from typing import Optional
from dataclasses import dataclass, asdict, field
from ...utils.json import json_dumps

@dataclass
class UserComponent:
    dictKey: Optional[int]
    idambient: Optional[int]
    idsf: Optional[int]
    name: Optional[str]
    sftype: Optional[str]
    sstype: Optional[str]
    
    _elements: list[UserElement] = field(default_factory=list)

    def to_json(self):
        return json_dumps(asdict(self))
    
    def to_tuple(self) -> tuple:
        return (
            self.dictKey,
            self.idambient,
            self.idsf,
            self.name,
            self.sftype,
            self.sstype
        )
        
    @staticmethod
    def list_from_dict(response: dict) -> list['UserComponent']:
        components = []
        for result in response['result']:
            id_ambient = result['idambient']
            sfs = result['sf']
            ambient_components = UserComponent._list_from_dict(id_ambient, sfs)
            components.extend(ambient_components)
        return components
    
    @staticmethod
    def _list_from_dict(id_ambient: str, sfs: list[dict]) -> 'UserComponent':
        components = []
        for sf in sfs:
            component = UserComponent._obj_from_dict(id_ambient, sf)
            components.append(component)
        return components
    
    @staticmethod
    def _obj_from_dict(id_ambient: str, sf: dict) -> 'UserComponent':
        id_component = sf['idsf']
        elements = sf['elements']
        return UserComponent(
            idambient = id_ambient,
            dictKey = sf['dictKey'],
            idsf = sf['idsf'],
            name = sf['name'],
            sftype = sf['sftype'],
            sstype = sf['sstype'],
            _elements = UserElement.list_from_dict(id_component, elements)
        )