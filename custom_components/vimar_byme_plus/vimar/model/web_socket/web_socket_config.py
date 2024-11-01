from typing import Optional, Callable
from ..gateway.gateway_info import GatewayInfo
from ..repository.user_credentials import UserCredentials
from ...model.web_socket.base_request_response import BaseRequestResponse


class WebSocketConfig:
    address: str
    port: str
    gateway_info: GatewayInfo
    user_credentials: UserCredentials
    on_open_callback: Optional[Callable[[], None]] = None
    on_close_callback: Optional[Callable[[BaseRequestResponse], None]] = None
    on_message_callback: Optional[
        Callable[[BaseRequestResponse], BaseRequestResponse]
    ] = None
    on_error_message_callback: Optional[
        Callable[
            [BaseRequestResponse, BaseRequestResponse, Exception], BaseRequestResponse
        ]
    ] = None
