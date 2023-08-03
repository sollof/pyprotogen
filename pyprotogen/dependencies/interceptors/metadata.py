from collections import OrderedDict
from typing import Callable


from grpc.aio import ClientCallDetails
from grpc.aio import UnaryUnaryCall
from grpc.aio import UnaryUnaryClientInterceptor
from grpc.aio._typing import RequestType
from grpc.aio._typing import ResponseType


class MetadataClientInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, client_name: str) -> None:
        self.client_name = client_name

    def propagate_metadata_in_details(
        self,
        client_call_details: ClientCallDetails
    ) -> ClientCallDetails:
        metadata = client_call_details.metadata
        if not metadata:
            mutable_metadata = OrderedDict()
        else:
            mutable_metadata = OrderedDict(metadata)

        mutable_metadata['client_name'] = self.client_name
        metadata = tuple(mutable_metadata.items())

        return ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
            client_call_details.wait_for_ready,
        )

    async def intercept_unary_unary(
        self,
        continuation: Callable[[ClientCallDetails, RequestType], UnaryUnaryCall],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> UnaryUnaryCall | ResponseType:
        client_call_details_with_metadata = self.propagate_metadata_in_details(client_call_details)
        return await continuation(client_call_details_with_metadata, request)
