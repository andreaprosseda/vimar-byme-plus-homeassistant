from dataclasses import dataclass

from ..base_request import BaseRequest


@dataclass
class GetStatusRequest(BaseRequest):
    def __init__(self, target: str, token: str, msgid: str, idsf: int):
        super().__init__()
        self.function = "getstatus"
        self.target = target
        self.token = token
        self.msgid = str(msgid)
        self.args = [self.get_argument(idsf)]

    # def get_args(self, idsf: str) -> list:
    #     return [self.get_argument(action) for action in actions]

    def get_argument(self, idsf: int) -> dict:
        return {"idsf": idsf, "sfetype": []}
