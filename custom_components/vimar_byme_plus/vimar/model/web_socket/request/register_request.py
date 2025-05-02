from dataclasses import dataclass

from ...repository.user_component import UserComponent
from ..base_request import BaseRequest


@dataclass
class RegisterRequest(BaseRequest):
    def __init__(self, target: str, token: str, components: list[UserComponent]):
        super().__init__()
        self.function = "register"
        self.target = target
        self.token = token
        self.msgid = "3"
        self.args = self.get_args(components)

    def get_args(self, components: list[UserComponent]) -> list:
        arguments = []
        for component in components:
            arguments.append(self.get_argument(component))
        return arguments

    def get_argument(self, component: UserComponent) -> dict:
        return {"idsf": component.idsf, "sfetype": self.get_sfe_types(component)}

    def get_sfe_types(self, component: UserComponent) -> list[str]:
        return [element.sfetype for element in component.elements]
