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
    def list_from_response(response: dict) -> list['UserComponent']:
        components = []
        for result in response.get('result', []):
            ambient_components = UserComponent.list_from_result(result)
            components.extend(ambient_components)
        return components
            
    @staticmethod
    def list_from_request(response: dict) -> list['UserComponent']:
        components = []
        for arg in response.get('args', []):
            component = UserComponent._obj_from_sf(None, arg)
            components.append(component)
        return components

    @staticmethod
    def list_from_result(result: dict) -> list['UserComponent']:
        id_ambient = result.get('idambient')
        sfs = result.get('sf', [])
        return UserComponent._list_from_sfs(id_ambient, sfs)
    
    @staticmethod
    def _list_from_sfs(id_ambient: str, sfs: list[dict]) -> 'UserComponent':
        components = []
        for sf in sfs:
            component = UserComponent._obj_from_sf(id_ambient, sf)
            components.append(component)
        return components
    
    @staticmethod
    def _obj_from_sf(id_ambient: str, sf: dict) -> 'UserComponent':
        id_component = sf.get('idsf')
        elements = sf.get('elements', [])
        return UserComponent(
            idambient = id_ambient,
            dictKey = sf.get('dictKey'),
            idsf = sf.get('idsf'),
            name = sf.get('name'),
            sftype = sf.get('sftype'),
            sstype = sf.get('sstype'),
            _elements = UserElement.list_from_dict(id_component, elements)
        )