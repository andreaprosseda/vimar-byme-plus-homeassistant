from zeroconf import ServiceInfo

class GatewayInfo:
    server: str
    address: str
    port: str
    model: str
    deviceuid: str
    mac: str
    softwareversion: str
    protocolversion: str
    communicationmode: str
    plantuid: str
    plantname: str
    devicename: str
    uuid1: str
    uuid2: str
    ntpmode: str
    
    def __init__(self, info: ServiceInfo):
        self.server = info.server
        self.address = '.'.join(map(str, info.addresses[0]))
        self.port = info.port
        
        props: dict = {key.decode(): value.decode() for key, value in info.properties.items()}
        self.model = props.get('model')
        self.deviceuid = props.get('deviceuid')
        self.mac = props.get('mac')
        self.softwareversion = props.get('softwareversion')
        self.protocolversion = props.get('protocolversion')
        self.communicationmode = props.get('communicationmode')
        self.plantuid = props.get('plantuid')
        self.plantname = props.get('plantname')
        self.devicename = props.get('devicename')
        self.uuid1 = props.get('uuid1')
        self.uuid2 = props.get('uuid2')
        self.ntpmode = props.get('ntpmode')
            
    def __repr__(self):
        return f"Gateway(name={self.plantname}, server={self.server}, address={self.address}, port={self.port})"
