from dataclasses import dataclass
from ..base_request import BaseRequest
from ..supporting_models.argument import Argument
from ..supporting_models.communication import Communication, CommunicationMode

@dataclass
class SessionRequest(BaseRequest):

    def __init__(self, target: str, token: str):
        super().__init__()
        self.function = 'session'
        self.target = target
        self.token = token
        self.msgid = '0'
        self.args = self.get_args()

    def get_args(self) -> list:
        communication = self.get_communication()
        argument = Argument(communication)
        return [argument]
    
    def get_communication(self) -> Communication:
        return Communication(
            address='192.168.1.132',
            port=0,
            mode=CommunicationMode.WEB_SOCKET
        )