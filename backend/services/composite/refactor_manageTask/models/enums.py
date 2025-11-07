from enum import Enum

class HttpStatus(Enum):
    """HTTP status codes used in the application"""
    OK = 200
    NO_CONTENT = 204
    NOT_FOUND = 404
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    INTERNAL_ERROR = 500