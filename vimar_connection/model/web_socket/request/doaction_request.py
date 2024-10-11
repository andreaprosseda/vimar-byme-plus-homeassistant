from dataclasses import dataclass
from ..base_request import BaseRequest
from ...repository.user_element import UserElement

@dataclass
class DoActionRequest(BaseRequest):

    def __init__(self, target: str, token: str, msgid: str, elements: list[UserElement]):
        super().__init__()
        self.function = 'doaction'
        self.target = target
        self.token = token
        self.msgid = str(msgid)
        self.args = self.get_args(elements)

    def get_args(self, elements: list[UserElement]) -> list:
        arguments = []
        for element in elements:
            arguments.append(self.get_argument(element))
        return arguments
    
    def get_argument(self, element: UserElement) -> dict:
        return {
            'idsf' : element.idcomponent,
            'sfetype' : element.sfetype,
            'value' : element.value
        }