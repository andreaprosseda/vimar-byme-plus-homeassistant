from dataclasses import asdict, dataclass, field

from ...utils.json import json_dumps
from ..enum.sfetype_enum import SfeType
from ..web_socket.base_request import BaseRequest
from ..web_socket.base_response import BaseResponse
from .user_ambient import UserAmbient
from .user_element import UserElement


@dataclass
class UserComponent:
    dictKey: int | None
    idambient: int | None
    idsf: int | None
    name: str | None
    sftype: str | None
    sstype: str | None
    ambient: UserAmbient | None = None
    elements: list[UserElement] = field(default_factory=list)

    def to_json(self):
        return json_dumps(asdict(self))

    def to_tuple(self) -> tuple:
        return (
            self.dictKey,
            self.idambient,
            self.idsf,
            self.name,
            self.sftype,
            self.sstype,
        )

    def is_enabled(self, sfetype: SfeType) -> bool:
        for element in self.elements:
            if element.sfetype == sfetype.value:
                return element.enable
        return False

    def get_value(self, sfetype: SfeType) -> str:
        for element in self.elements:
            if element.sfetype == sfetype.value:
                return element.value
        return None

    def get_last_update(self, sfetype: SfeType) -> str:
        for element in self.elements:
            if element.sfetype == sfetype.value:
                return element.last_update
        return None

    @staticmethod
    def list_from_response(response: BaseResponse) -> list["UserComponent"]:
        components = []
        for result in response.result:
            ambient_components = UserComponent.list_from_result(result)
            components.extend(ambient_components)
        return components

    @staticmethod
    def list_from_request(request: BaseRequest) -> list["UserComponent"]:
        components = []
        for arg in request.args:
            component = UserComponent._obj_from_sf(None, arg)
            components.append(component)
        return components

    @staticmethod
    def list_from_result(result: dict) -> list["UserComponent"]:
        id_ambient = result.get("idambient")
        sfs = result.get("sf", [])
        return UserComponent._list_from_sfs(id_ambient, sfs)

    @staticmethod
    def _list_from_sfs(id_ambient: str, sfs: list[dict]) -> "UserComponent":
        components = []
        for sf in sfs:
            component = UserComponent._obj_from_sf(id_ambient, sf)
            components.append(component)
        return components

    @staticmethod
    def _obj_from_sf(id_ambient: str, sf: dict) -> "UserComponent":
        id_component = sf.get("idsf")
        elements = sf.get("elements", [])
        return UserComponent(
            idambient=id_ambient,
            dictKey=sf.get("dictKey"),
            idsf=sf.get("idsf"),
            name=sf.get("name"),
            sftype=sf.get("sftype"),
            sstype=sf.get("sstype"),
            ambient=None,
            elements=UserElement.list_from_dict(id_component, elements),
        )
