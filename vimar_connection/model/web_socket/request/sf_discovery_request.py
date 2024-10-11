from dataclasses import dataclass
from ..base_request import BaseRequest
from ..supporting_models.argument import Argument
from ..supporting_models.parameter import Parameter

@dataclass
class SfDiscoveryRequest(BaseRequest):

    def __init__(self, target: str, token: str, ambient_ids: list[str]):
        super().__init__()
        self.function = 'sfdiscovery'
        self.target = target
        self.token = token
        self.msgid = '2'
        self.args = self.get_args()
        self.params = self.get_params(ambient_ids)

    def get_args(self) -> list:
        argument = Argument(sfcategory = 'Plant')
        return [argument]
    
    def get_params(self, ambient_ids: list[int]) -> list:
        parameter = Parameter(ambient_ids = ambient_ids)
        return [parameter]