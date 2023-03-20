from grpc.aio import ClientCallDetails


def split_method_call(
    handler_call_details: ClientCallDetails,
) -> tuple[str, str, bool]:  # pragma: no cover
    method = handler_call_details.method
    if isinstance(method, bytes):
        # https://github.com/grpc/grpc/issues/31092
        method = method.decode()
    parts = method.split("/")
    if len(parts) < 3:
        return "", "", False

    grpc_service_name, grpc_method_name = parts[1:3]
    return grpc_service_name, grpc_method_name, True
