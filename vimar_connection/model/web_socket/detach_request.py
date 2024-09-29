from .base_request import BaseRequest
from .supporting_models.argument import Argument
from dataclasses import dataclass

@dataclass
class DetachRequest(BaseRequest):

    def __init__(self, target: str, token: str):
        super().__init__()
        self.function = 'detach'
        self.target = target
        self.token = token
        self.msgid = '1'
        self.args = self.get_args()

    def get_args(self) -> list:
        argument = self.get_argument()
        return [argument]
    
    def get_argument(self) -> Argument:
        return Argument(
            user = 'logout'
        )