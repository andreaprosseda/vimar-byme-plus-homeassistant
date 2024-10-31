from dataclasses import dataclass
from ..enum.sfetype_enum import SfeType


@dataclass
class VimarAction:
    idsf: str
    sfetype: SfeType
    value: str
