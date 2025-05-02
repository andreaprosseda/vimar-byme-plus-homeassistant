from dataclasses import dataclass

from ...repository.user_credentials import UserCredentials
from ..base_request import BaseRequest
from ..supporting_models.client_info import ClientInfo
from ..supporting_models.communication import Communication
from ..supporting_models.credential import Credential


@dataclass
class AttachRequest(BaseRequest):
    def __init__(
        self,
        target: str,
        token: str,
        protocol_version: str,
        user_credentials: UserCredentials,
        ip_address: str,
    ):
        super().__init__()
        self.function = "attach"
        self.target = target
        self.token = token
        self.msgid = "0"
        self.args = self.get_args(protocol_version, user_credentials, ip_address)

    def get_args(
        self, protocol_version: str, user_credentials: UserCredentials, ip_address: str
    ) -> list:
        credential = self.get_credential(user_credentials)
        client_info = self.get_client_info(user_credentials, protocol_version)
        communication = self.get_communication(ip_address)
        argument = self.get_argument(credential, client_info, communication)
        return [argument]

    def get_credential(self, credentials: UserCredentials) -> Credential:
        return Credential(
            username=credentials.username,
            useruid=credentials.useruid,
            password=credentials.password,
        )

    def get_client_info(
        self, credentials: UserCredentials, protocol_version: str
    ) -> ClientInfo:
        return ClientInfo(
            client_tag="thirdpartyapp",
            sf_model_version="1.0.0",
            protocol_version=protocol_version,
            manufacturer_tag=credentials.username,
        )

    def get_communication(self, ip_address: str) -> Communication:
        return Communication(address=ip_address)

    def get_argument(
        self,
        credential: Credential,
        client_info: ClientInfo,
        communication: Communication,
    ):
        return {
            "credential": credential,
            "clientinfo": client_info,
            "communication": communication,
        }
