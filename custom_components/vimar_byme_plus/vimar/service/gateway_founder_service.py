from zeroconf import Zeroconf, ServiceBrowser, ServiceListener, ServiceInfo
from ..model.gateway.gateway_info import GatewayInfo
from ..config.const import GATEWAY_SERVICE_TYPE
from ..utils.logger import log_info


class GatewayFounderService(ServiceListener):
    gateway_info: GatewayInfo = None

    def search(self) -> GatewayInfo:
        log_info(__name__, f"Searching for {GATEWAY_SERVICE_TYPE} services...\n")
        service_browser: ServiceBrowser = None
        zeroconf = Zeroconf()
        try:
            service_browser = ServiceBrowser(zeroconf, GATEWAY_SERVICE_TYPE, self)
            while not self.gateway_info:
                pass  # waiting for gateway to be found
        except KeyboardInterrupt:
            log_info(__name__, "Search interrupted.")
        finally:
            zeroconf.close()
            service_browser.cancel()
        return self.gateway_info

    def add_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        log_info(__name__, f"Service Found: {info.server}")

        if self.is_vimar_gateway(info):
            self.gateway_info = self.get_vimar_gateway_info(info)
            log_info(__name__, f"Gateway Found!\n{self.gateway_info}")
        else:
            log_info(__name__, "Not Vimar Gateway, still searching...\n")

    def remove_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        log_info(__name__, "remote_service method invoked")

    def update_service(self, zc: "Zeroconf", type_: str, name: str) -> None:
        log_info(__name__, "update_service method invoked")

    def is_vimar_gateway(self, info: ServiceInfo | None) -> bool:
        return info and info.properties.get(b"model", b"") == b"AG+"

    def get_vimar_gateway_info(self, info: ServiceInfo) -> GatewayInfo:
        address = ".".join(map(str, info.addresses[0]))
        properties = info.properties.items()
        props = {key.decode(): value.decode() for key, value in properties}
        return GatewayInfo.from_info(
            server=info.server,
            address=address,
            port=info.port,
            props=props
        )