from zeroconf import Zeroconf, ServiceBrowser, ServiceListener, ServiceInfo
from ..model.gateway.gateway_info import GatewayInfo
from ..config.const import GATEWAY_SERVICE_TYPE

class GatewayFounderService(ServiceListener):
    
    gateway_info: GatewayInfo = None
    
    def search(self) -> GatewayInfo:
        print(f"Searching for {GATEWAY_SERVICE_TYPE} services...\n")
        zeroconf = Zeroconf()
        try:
            ServiceBrowser(zeroconf, GATEWAY_SERVICE_TYPE, self)
            while(not self.gateway_info):
                pass # waiting for gateway to be found
        except KeyboardInterrupt:
            print("Search interrupted.")
        finally:
            zeroconf.close()
        return self.gateway_info
        
    def add_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service Found: {info.server}")
        
        if self.is_vimar_gateway(info):
            self.gateway_info = GatewayInfo(info)
            print(f"Gateway Found!\n{self.gateway_info}")
        else:
            print("Not Vimar Gateway, still searching...\n")
        
    def remove_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        print("remote_service method invoked")

    def update_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        print("update_service method invoked")
        
    def is_vimar_gateway(self, info: ServiceInfo | None) -> bool:
        return info and info.properties.get(b'model', b'') == b'AG+'