from dataclasses import dataclass, asdict
from ...utils.json import json_dumps
from ..web_socket.base_response import BaseResponse
from zeroconf import ServiceInfo


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

    def __init__(self):
        self.plantname = "Cruizer"
        self.port = 20615
        self.server = "AG-3A2643FBB24000.local."
        self.address = "192.168.1.50"
        self.deviceuid = "3A2643FBB24000"
        self.protocolversion = "2.7"

    # def __init__(self, info: ServiceInfo):
    #     self.server = info.server
    #     self.address = ".".join(map(str, info.addresses[0]))
    #     self.port = info.port

    #     props: dict = {
    #         key.decode(): value.decode() for key, value in info.properties.items()
    #     }
    #     self.model = props.get("model")
    #     self.deviceuid = props.get("deviceuid")
    #     self.mac = props.get("mac")
    #     self.softwareversion = props.get("softwareversion")
    #     self.protocolversion = props.get("protocolversion")
    #     self.communicationmode = props.get("communicationmode")
    #     self.plantuid = props.get("plantuid")
    #     self.plantname = props.get("plantname")
    #     self.devicename = props.get("devicename")
    #     self.uuid1 = props.get("uuid1")
    #     self.uuid2 = props.get("uuid2")
    #     self.ntpmode = props.get("ntpmode")

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json_dumps(asdict(self))

    def __repr__(self):
        return f"Gateway(name={self.plantname}, server={self.server}, address={self.address}, port={self.port})"
