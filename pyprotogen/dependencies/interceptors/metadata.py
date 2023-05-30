from typing import Callable

from grpc.aio import ClientCallDetails
from grpc.aio import UnaryUnaryCall
from grpc.aio import UnaryUnaryClientInterceptor
from grpc.aio._typing import RequestType
from grpc.aio._typing import ResponseType


class MetadataClientInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, client_name: str) -> None:
        self.client_name = client_name

    async def intercept_unary_unary(
        self,
        continuation: Callable[[ClientCallDetails, RequestType], UnaryUnaryCall],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> UnaryUnaryCall | ResponseType:
        client_call_details.metadata.add('client-name', self.client_name)
        return await continuation(client_call_details, request)
