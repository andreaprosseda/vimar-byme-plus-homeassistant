from dataclasses import asdict, dataclass

from ...utils.json import json_dumps


@dataclass
class AssociationRequest:
    username: str
    setup_code: str

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json_dumps(asdict(self))
