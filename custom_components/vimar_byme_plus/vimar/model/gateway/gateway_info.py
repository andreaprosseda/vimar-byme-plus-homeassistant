from dataclasses import dataclass, asdict
from ...utils.json import json_dumps

@dataclass
class GatewayInfo:
    server: str | None = None
    address: str | None = None
    port: str | None = None
    model: str | None = None
    deviceuid: str | None = None
    mac: str | None = None
    softwareversion: str | None = None
    protocolversion: str | None = None
    communicationmode: str | None = None
    plantuid: str | None = None
    plantname: str | None = None
    devicename: str | None = None
    uuid1: str | None = None
    uuid2: str | None = None
    ntpmode: str | None = None

    @classmethod
    def from_mocked_values(cls):
        return cls(
            server="AG-3A2643FBB24000.local.",
            address="192.168.1.50",
            port=20615,
            model=None,
            deviceuid="3A2643FBB24000",
            mac=None,
            softwareversion=None,
            protocolversion="2.7",
            communicationmode=None,
            plantuid=None,
            plantname="Cruizer",
            devicename=None,
            uuid1=None,
            uuid2=None,
            ntpmode=None,
        )

    @classmethod
    def from_info(cls, server: str, address: str, port: int, props: dict):
        return cls(
            server=server,
            address=address,
            port=port,
            model=props.get("model"),
            deviceuid=props.get("deviceuid"),
            mac=props.get("mac"),
            softwareversion=props.get("softwareversion"),
            protocolversion=props.get("protocolversion"),
            communicationmode=props.get("communicationmode"),
            plantuid=props.get("plantuid"),
            plantname=props.get("plantname"),
            devicename=props.get("devicename"),
            uuid1=props.get("uuid1"),
            uuid2=props.get("uuid2"),
            ntpmode=props.get("ntpmode"),
        )
        
    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json_dumps(asdict(self))

    def __repr__(self):
        return f"Gateway(name={self.plantname}, server={self.server}, address={self.address}, port={self.port})"
