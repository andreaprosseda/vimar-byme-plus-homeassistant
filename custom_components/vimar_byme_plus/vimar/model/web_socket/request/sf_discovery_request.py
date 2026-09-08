from dataclasses import dataclass

from ..base_request import BaseRequest
from ..supporting_models.parameter import Parameter


@dataclass
class SfDiscoveryRequest(BaseRequest):
    def __init__(
        self, target: str, token: str, ambient_ids: list[str], sfcategory: str
    ):
        super().__init__()
        self.function = "sfdiscovery"
        self.target = target
        self.token = token
        self.msgid = "2"
        self.args = self.get_args(sfcategory)
        self.params = self.get_params(ambient_ids)

    def get_args(self, sfcategory: str) -> list:
        return [self.get_category(sfcategory)]

    def get_category(self, value: str) -> dict:
        return {"sfcategory": value}

    def get_params(self, ambient_ids: list[int]) -> list:
        parameter = Parameter(ambient_ids=ambient_ids)
        return [parameter]
