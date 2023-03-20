from enum import Enum


class GrpcType(Enum):
    UNARY = "unary"
    SERVER_STREAMING = "server_streaming"
    CLIENT_STREAMING = "client_streaming"
    BIDI_STREAMING = "bidi_streaming"
    UNKNOWN = "unknown"
