from dataclasses import dataclass
from ..base_request import BaseRequest
from ..supporting_models.communication import Communication, CommunicationMode
from ....utils.ip_address import get_ip_address


@dataclass
class SessionRequest(BaseRequest):
    def __init__(self, target: str, token: str):
        super().__init__(
            function="session",
            target=target,
            token=token,
            msgid="0",
            args=self.get_args(),
        )

    def get_args(self) -> list:
        communication = self.get_communication()
        argument = self.get_argument(communication)
        return [argument]

    def get_argument(self, communication: Communication) -> dict:
        return {"communication": communication}

    def get_communication(self) -> Communication:
        return Communication(
            address=get_ip_address(), port=0, mode=CommunicationMode.WEB_SOCKET
        )
