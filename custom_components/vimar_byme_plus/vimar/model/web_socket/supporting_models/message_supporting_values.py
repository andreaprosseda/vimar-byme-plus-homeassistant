from dataclasses import dataclass

@dataclass
class MessageSupportingValues:
    target: str
    token: str
    msgid: str
    protocol_version: str
    