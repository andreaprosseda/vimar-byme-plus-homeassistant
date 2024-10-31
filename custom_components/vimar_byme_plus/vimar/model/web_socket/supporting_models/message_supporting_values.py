from dataclasses import dataclass
from ...component.vimar_action import VimarAction


@dataclass
class MessageSupportingValues:
    target: str
    token: str
    msgid: str
    protocol_version: str
    actions: list[VimarAction]
