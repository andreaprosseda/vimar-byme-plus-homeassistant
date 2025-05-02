from dataclasses import dataclass

from ..base_request import BaseRequest


@dataclass
class KeepAliveRequest(BaseRequest):
    def __init__(self, target: str, token: str, msgid: int):
        super().__init__()
        self.function = "keepalive"
        self.target = target
        self.token = token
        self.msgid = str(msgid)
