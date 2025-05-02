from collections.abc import Callable

from ...model.web_socket.base_request_response import BaseRequestResponse
from ..gateway.gateway_info import GatewayInfo
from ..repository.user_credentials import UserCredentials


class WebSocketConfig:
    address: str
    port: str
    gateway_info: GatewayInfo
    user_credentials: UserCredentials
    on_open_callback: Callable[[], None] | None = None
    on_close_callback: Callable[[BaseRequestResponse], None] | None = None
    on_message_callback: Callable[[BaseRequestResponse], BaseRequestResponse] | None = (
        None
    )
    on_error_message_callback: (
        Callable[
            [BaseRequestResponse, BaseRequestResponse, Exception], BaseRequestResponse
        ]
        | None
    ) = None
