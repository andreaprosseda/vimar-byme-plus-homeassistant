"""Provides the Vimar DataUpdateCoordinator."""
import requests
from typing import Any
from ..model.repository.user_credentials import UserCredentials
from ..model.authenticator.association_request import AssociationRequest
from ..model.authenticator.operational_request import OperationalRequest
from ..model.authenticator.credential_response import CredentialResponse
from ..model.exceptions import VimarErrorResponseException
from ..utils.logger import log_debug

class AuthenticatorClient:
    """Class to manage signed setup_code and password for VIMAR connection."""

    URL = "https://vimar-byme-plus-authenticator.onrender.com"
    
    def get_association_credentials(self, credentials: UserCredentials) -> UserCredentials:
        request = self._get_association_request(credentials)
        response = self._get_association_credentials(request)
        return self._get_user_credentials(response)

    def get_operational_credentials(self, credentials: UserCredentials) -> UserCredentials:
        request = self._get_operational_request(credentials)
        response = self._get_operational_credentials(request)
        return self._get_user_credentials(response)
    
    def _get_association_credentials(self, request: AssociationRequest) -> CredentialResponse:
        url = self.URL + "/api/vimar/phases/association/credentials"
        request_json = request.to_dict()
        log_debug(__name__, f"Sending json:\n{request_json}")
        response = requests.post(url, json=request_json)
        response_json = response.json()
        if response.ok:
            log_debug(__name__, f"Response received:\n{response_json}")
            return CredentialResponse(**response_json)
        message = f"Error receiving association signed credentials:\n{response_json}"
        raise VimarErrorResponseException(message)
        

    def _get_operational_credentials(self, request: OperationalRequest) -> CredentialResponse:
        url = self.URL + "/api/vimar/phases/operational/credentials"
        request_json = request.to_dict()
        log_debug(__name__, f"Sending json:\n{request_json}")
        response = requests.post(url, json=request_json)
        response_json = response.json()
        if response.ok:
            log_debug(__name__, f"Response received:\n{response_json}")
            return CredentialResponse(**response_json)
        message = f"Error receiving operational signed credentials:\n{response_json}"
        raise VimarErrorResponseException(message)
    
    def _get_association_request(self, credentials: UserCredentials) -> AssociationRequest:
        return AssociationRequest(
            username=credentials.username,
            setup_code=credentials.setup_code
        )
    
    def _get_operational_request(self, credentials: UserCredentials) -> OperationalRequest:
        return OperationalRequest(
            username=credentials.username,
            userid=credentials.useruid,
            password=credentials.password
        )
    
    def _get_user_credentials(self, response: CredentialResponse) -> UserCredentials:
        return UserCredentials(
            username=response.username,
            useruid=response.userid,
            password=response.password
        )