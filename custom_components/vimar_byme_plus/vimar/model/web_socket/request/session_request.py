from dataclasses import dataclass

from ..base_request import BaseRequest
from ..supporting_models.communication import Communication, CommunicationMode


@dataclass
class SessionRequest(BaseRequest):
    def __init__(self, target: str, token: str, ip_address: str):
        super().__init__(
            function="session",
            target=target,
            token=token,
            msgid="0",
            args=self.get_args(ip_address),
        )

    def get_args(self, ip_address: str) -> list:
        communication = self.get_communication(ip_address)
        argument = self.get_argument(communication)
        return [argument]

    def get_argument(self, communication: Communication) -> dict:
        return {"communication": communication}

    def get_communication(self, ip_address: str) -> Communication:
        return Communication(
            address=ip_address, port=0, mode=CommunicationMode.WEB_SOCKET
        )
