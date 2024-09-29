from .gateway_founder import GatewayFounder
from .client.vimar_client import VimarClient
from .database.database import Database

if __name__ == "__main__":
    database = Database('home.db')
    founder = GatewayFounder()
    gateway_info = founder.search()
    vimar_client = VimarClient(gateway_info)
    vimar_client.connect()