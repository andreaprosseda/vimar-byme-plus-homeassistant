from dataclasses import dataclass, asdict
from ...utils.json import json_dumps


@dataclass
class GatewayInfo:
    address: str | None = None
    port: str | None = None
    deviceuid: str | None = None
    host: str | None = None
    plantname: str | None = None
    protocolversion: str | None = None

    @classmethod
    def from_mocked_values(cls):
        return cls(
            host="AG-3A2643FBB24000.local.",
            address="192.168.1.50",
            port=20615,
            deviceuid="3A2643FBB24000",
            plantname="Cruizer",
            protocolversion="2.7",
        )

    @classmethod
    def from_info(cls, host: str, address: str, port: int, props: dict):
        return cls(
            host=host,
            address=address,
            port=port,
            deviceuid=props.get("deviceuid"),
            plantname=props.get("plantname"),
            protocolversion=props.get("protocolversion"),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json_dumps(asdict(self))

    def __repr__(self):
        return f"Gateway(name={self.plantname}, host={self.host}, address={self.address}, port={self.port})"
