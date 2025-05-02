from dataclasses import dataclass

from ...component.vimar_action import VimarAction
from ..base_request import BaseRequest


@dataclass
class DoActionRequest(BaseRequest):
    def __init__(self, target: str, token: str, msgid: str, actions: list[VimarAction]):
        super().__init__()
        self.function = "doaction"
        self.target = target
        self.token = token
        self.msgid = str(msgid)
        self.args = self.get_args(actions)

    def get_args(self, actions: list[VimarAction]) -> list:
        return [self.get_argument(action) for action in actions]

    def get_argument(self, action: VimarAction) -> dict:
        return {
            "idsf": action.idsf,
            "sfetype": action.sfetype,
            "value": action.value,
        }
