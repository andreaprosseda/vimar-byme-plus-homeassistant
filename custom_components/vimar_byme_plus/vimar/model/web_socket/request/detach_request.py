from dataclasses import dataclass

from ..base_request import BaseRequest


@dataclass
class DetachRequest(BaseRequest):
    def __init__(self, target: str, token: str, msgid: str):
        super().__init__()
        self.function = "detach"
        self.target = target
        self.token = token
        self.msgid = str(msgid)
        self.args = self.get_args()

    def get_args(self) -> list:
        argument = self.get_argument()
        return [argument]

    def get_argument(self) -> dict:
        return {"user": "logout"}
