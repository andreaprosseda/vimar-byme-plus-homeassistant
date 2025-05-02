from dataclasses import asdict, dataclass

from ...utils.json import json_dumps


@dataclass
class BaseRequestResponse:
    type: str
    function: str
    source: str
    target: str
    token: str
    msgid: str

    def to_json(self) -> str:
        return json_dumps(asdict(self))
