from ...model.web_socket.base_response import BaseResponse
from ...model.gateway.gateway_info import GatewayInfo
from ...model.web_socket.base_request_response import BaseRequestResponse
from ...utils.logger import log_info
from ...model.enum.error_response_enum import ErrorResponse
from ...config.const import DATABASE_NAME
from ...utils.file import remove_file

class ErrorHandler:
    
    _gateway_info: GatewayInfo
    
    def __init__(self, gateway_info: GatewayInfo):
        self._gateway_info = gateway_info
    
    def error_message_received(self, last_client_message: BaseRequestResponse, last_server_message: BaseRequestResponse, exception: Exception) -> BaseRequestResponse:
        if self.is_temporary_error(exception):
            return self.handle_temporary_error(last_client_message)
        if self.is_permanent_error(last_server_message):
            return self.handle_permanent_error()
        return None
    
    def is_temporary_error(self, exception: Exception) -> bool:
        if self.is_ssl_error(exception):
            return True
        return False

    def is_permanent_error(self, message: BaseRequestResponse) -> BaseRequestResponse:
        if self.is_vimar_permanent_error(message):
            return True
        return False
    
    def handle_temporary_error(self, last_client_message: BaseRequestResponse) -> BaseRequestResponse:
        return last_client_message
    
    def handle_permanent_error(self):
        log_info(__name__, f"Removing database {DATABASE_NAME} ...")
        remove_file(DATABASE_NAME)
        raise ConnectionAbortedError()
        
    def is_ssl_error(self, exception: Exception) -> bool:
        error_type = type(exception).__name__
        if error_type == 'SSLError':
            log_info(__name__, "SSLError, sending new message...")
            return True
        if error_type == 'SSLEOFError':
            log_info(__name__, "SSLError, sending new message...")
            return True
        return False
    
    def is_vimar_permanent_error(self, message: BaseRequestResponse) -> bool:
        if isinstance(message, BaseResponse):
            errors = [
                ErrorResponse.IP_CONNECTOR_ERR_INVALID_PWD, 
                ErrorResponse.IP_CONNECTOR_ERR_PERMISSION_DENIED
            ]
            values = [error.value for error in errors]
            if message.error in values:
                return True
        