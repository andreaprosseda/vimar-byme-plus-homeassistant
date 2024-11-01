from dataclasses import dataclass


@dataclass
class CredentialResponse:
    username: str
    userid: str
    password: str
