from enum import Enum

class ErrorResponse(Enum):
    IP_CONNECTOR_NO_ERR = 0
    IP_CONNECTOR_ERR_MALFORMED_MESSAGE = 1
    IP_CONNECTOR_ERR_PERMISSION_DENIED = 2
    IP_CONNECTOR_ERR_INVALID_TARGET = 3
    IP_CONNECTOR_ERR_INVALID_SOURCE = 4
    IP_CONNECTOR_ERR_INVALID_TOKEN = 5
    IP_CONNECTOR_ERR_INVALID_TYPE = 6
    IP_CONNECTOR_ERR_MALFORMED_ARGS = 7
    IP_CONNECTOR_ERR_UNKNOWN_FUNCTION = 8
    IP_CONNECTOR_ERR_UNIMPLEMENTED_FUNCTION = 9
    IP_CONNECTOR_ERR_DATA = 10
    IP_CONNECTOR_ERR_ELEMENT_VALUE = 11
    IP_CONNECTOR_ERR_USER_NOT_FOUND = 12
    IP_CONNECTOR_ERR_INVALID_CLIENT_TAG = 13
    IP_CONNECTOR_ERR_INVALID_COMM_MODE = 15
    IP_CONNECTOR_ERR_SESSION = 16
    IP_CONNECTOR_ERR_REMOVING_USER = 17
    IP_CONNECTOR_ERR_SCENE_NOT_CREATED = 18
    IP_CONNECTOR_ERR_SCENE_NOT_DELETED = 19
    IP_CONNECTOR_ERR_SCENE_NOT_SAVED = 20
    IP_CONNECTOR_ERR_INVALID_PWD = 21
    IP_CONNECTOR_ERR_SYSTEM_BLOCK = 23
    IP_CONNECTOR_ERR_SESSION_ALREADY_STARTED = 24
    IP_CONNECTOR_ERR_MALFORMED_PARAMS = 25
    IP_CONNECTOR_ERR_READING_DB = 27
    IP_CONNECTOR_ERR_PLANT_NOT_CONFIGURED = 28
    IP_CONNECTOR_ERR_LANG_NOT_SUPPORTED = 31
    IP_CONNECTOR_ERR_SYSTEM_LOADING = 34
    IP_CONNECTOR_ERR_INVALID_CONTEXT = 35
    
    @staticmethod
    def get_name_by_code(code: int) -> str:
        if code == 0:
            return None
        
        for elem in ErrorResponse:
            if elem.value == code:
                return elem.name
        
        return 'UNKNOWN_ERROR'