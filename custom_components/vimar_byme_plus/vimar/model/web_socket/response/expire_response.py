from dataclasses import dataclass

from ..base_response import BaseResponse


@dataclass
class ExpireResponse(BaseResponse):
    def __init__(self, target: str, token: str, msgid: int):
        super().__init__()
        self.function = "expire"
        self.target = target
        self.token = token
        self.msgid = str(msgid)
