from dataclasses import asdict, dataclass

from ...utils.json import json_dumps
from ..web_socket.base_response import BaseResponse


@dataclass
class UserAmbient:
    dictKey: str | None
    hash: str | None
    idambient: int | None
    idparent: int | None
    name: str | None

    def to_json(self):
        return json_dumps(asdict(self))

    def to_tuple(self) -> tuple:
        return (self.dictKey, self.hash, self.idambient, self.idparent, self.name)

    @staticmethod
    def list_from_dict(response: BaseResponse) -> list["UserAmbient"]:
        ambients = []
        for result in response.result:
            ambients.append(UserAmbient(**result))
        return ambients
