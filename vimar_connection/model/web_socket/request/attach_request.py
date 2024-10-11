from dataclasses import dataclass
from ..base_request import BaseRequest
from ..supporting_models.communication import Communication
from ..supporting_models.credential import Credential
from ..supporting_models.client_info import ClientInfo
from ...repository.user_credentials import UserCredentials
from ....utils.ip_address import get_ip_address
from ....utils.setup_code import sign_vimar_code

@dataclass
class AttachRequest(BaseRequest):

    def __init__(self, target: str, token: str, protocol_version: str, user_credentials: UserCredentials):
        super().__init__()
        self.function = 'attach'
        self.target = target
        self.token = token
        self.msgid = '0'
        self.args = self.get_args(protocol_version, user_credentials)

    def get_args(self, protocol_version: str, user_credentials: UserCredentials) -> list:
        credential = self.get_credential(user_credentials)
        client_info = self.get_client_info(protocol_version)
        communication = self.get_communication()
        argument = self.get_argument(credential, client_info, communication)
        return [argument]
    
    def get_credential(self, credentials: UserCredentials) -> Credential:
        password = credentials.password if credentials.password else credentials.setup_code
        useruid = credentials.useruid if credentials.useruid else ''
        return Credential(
            username = credentials.username,
            useruid = useruid,
            password = sign_vimar_code(password)
        )

    def get_client_info(self, protocol_version: str) -> ClientInfo:
        return ClientInfo(
            client_tag = 'thirdpartyapp',
            sf_model_version = '1.0.0',
            protocol_version = protocol_version,
            manufacturer_tag = 'xm7r1'
        )

    def get_communication(self) -> Communication:
        return Communication(address = get_ip_address())
    
    def get_argument(self, credential: Credential, client_info: ClientInfo, communication: Communication):
        return {
            'credential' : credential,
            'clientinfo' : client_info,
            'communication' : communication
        }