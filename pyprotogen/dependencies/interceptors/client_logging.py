import logging
from typing import Callable

from google.protobuf.json_format import MessageToJson  # type: ignore
from grpc import StatusCode
from grpc.aio import ClientCallDetails
from grpc.aio import UnaryUnaryCall
from grpc.aio import UnaryUnaryClientInterceptor
from grpc.aio._typing import RequestType
from grpc.aio._typing import ResponseType
from orjson import loads

from .dto import GrpcType
from .utils import split_method_call


class LoggingClientInterceptor(UnaryUnaryClientInterceptor):
    async def intercept_unary_unary(
        self,
        continuation: Callable[[ClientCallDetails, RequestType], UnaryUnaryCall],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> UnaryUnaryCall | ResponseType:
        handler = await continuation(client_call_details, request)
        code = await handler.code()
        if code != StatusCode.OK:
            service, method, _ = split_method_call(client_call_details)
            grpc_type = GrpcType.UNARY.value
            details = await handler.details()
            request_msg = loads(MessageToJson(request, preserving_proto_field_name=True))

            log_msg = 'grpc error'
            log_msg += f' | {service=}'
            log_msg += f' | {method=}'
            log_msg += f' | {grpc_type=}'
            log_msg += f' | {code=}'
            log_msg += f' | {details=}'
            log_msg += f' | {request_msg=}'

            logging.error(
                log_msg,
                extra={
                    'service': service,
                    'method': method,
                    'grpc_type': grpc_type,
                    'code': code,
                    'details': details,
                    'request_msg': request_msg,
                },
            )
        return handler
