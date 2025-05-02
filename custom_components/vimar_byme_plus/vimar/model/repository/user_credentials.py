from dataclasses import asdict, dataclass

from ...config.const import USERNAME
from ...utils.json import json_dumps
from ..web_socket.base_response import BaseResponse


@dataclass
class UserCredentials:
    username: str | None
    setup_code: str | None
    useruid: str | None
    password: str | None
    plant_name: str | None

    def __init__(
        self,
        username: str = None,
        useruid: str = None,
        password: str = None,
        setup_code: str = None,
        plant_name: str = None,
    ):
        self.username = username
        self.setup_code = setup_code
        self.useruid = useruid
        self.password = password
        self.plant_name = plant_name

    def to_json(self):
        return json_dumps(asdict(self))

    @staticmethod
    def obj_from_dict(response: BaseResponse) -> "UserCredentials":
        result = response.result[0]
        return UserCredentials(
            username=USERNAME,
            useruid=result["useruid"],
            password=result["password"],
            plant_name=result["plantname"],
        )
