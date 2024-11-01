from dataclasses import dataclass


@dataclass
class Credential:
    username: str
    useruid: str
    password: str

    def __init__(self, username: str, password: str, useruid: str):
        self.username = username
        self.password = password
        self.useruid = useruid
