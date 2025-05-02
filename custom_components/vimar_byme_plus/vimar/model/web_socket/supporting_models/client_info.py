from dataclasses import dataclass


@dataclass
class ClientInfo:
    clienttag: str
    sfmodelversion: str
    protocolversion: str
    manufacturertag: str | None = None

    def __init__(
        self,
        client_tag: str,
        sf_model_version: str,
        protocol_version: str,
        manufacturer_tag: str | None = None,
    ):
        self.clienttag = client_tag
        self.sfmodelversion = sf_model_version
        self.protocolversion = protocol_version
        self.manufacturertag = manufacturer_tag
