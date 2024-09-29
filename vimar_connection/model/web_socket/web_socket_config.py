from ..gateway_info import GatewayInfo
from ..user.user_credentials import UserCredentials
from typing import Optional, Callable
from ...model.web_socket.base_request import BaseRequest

class WebSocketConfig:
    address: str
    port: str
    gateway_info: GatewayInfo
    user_credentials: UserCredentials
    on_close_callback: Optional[Callable[[str], None]] = None
    on_message_callback: Optional[Callable[[str], BaseRequest]] = None
    on_error_message_callback: Optional[Callable[[str], BaseRequest]] = None