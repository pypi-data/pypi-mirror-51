import enum
import threading
import typing
from concurrent import futures
from typing_extensions import Literal

__version__: str

OptionKey = Literal[
    "grpc.census",
    "grpc.loadreporting",
    "grpc.minimal_stack",
    "grpc.max_concurrent_streams",
    "grpc.max_receive_message_length",
    "grpc.max_send_message_length",
    "grpc.max_connection_idle_ms",
    "grpc.max_connection_age_ms",
    "grpc.max_connection_age_grace_ms",
    "grpc.per_message_compression",
    "grpc.enable_deadline_checking",
    "grpc.http2.initial_sequence_number",
    "grpc.http2.lookahead_bytes",
    "grpc.http2.hpack_table_size.decoder",
    "grpc.http2.hpack_table_size.encoder",
    "grpc.http2.max_frame_size",
    "grpc.http2.bdp_probe",
    "grpc.http2.min_time_between_pings_ms",
    "grpc.http2_scheme",
    "grpc.http2.max_pings_without_data",
    "grpc.http2.max_ping_strikes",
    "grpc.http2.write_buffer_size",
    "grpc.http2.true_binary",
    "grpc.keepalive_time_ms",
    "grpc.keepalive_timeout_ms",
    "grpc.keepalive_permit_without_calls",
    "grpc.default_authority",
    "grpc.primary_user_agent",
    "grpc.secondary_user_agent",
    "grpc.min_reconnect_backoff_ms",
    "grpc.max_reconnect_backoff_ms",
    "grpc.initial_reconnect_backoff_ms",
    "grpc.server_handshake_timeout_ms",
    "grpc.ssl_target_name_override",
    "grpc.ssl_session_cache",
    "grpc.max_metadata_size",
    "grpc.so_reuseport",
    "grpc.resource_quota",
    "grpc.expand_wildcard_addrs",
    "grpc.service_config",
    "grpc.lb_policy_name",
    "grpc.socket_mutator",
    "grpc.socket_factory",
    "grpc.enable_channelz",
    "grpc.use_cronet_packet_coalescing",
    "grpc.grpclb_call_timeout_ms",
    "grpc.grpclb_fallback_timeout_ms",
    "grpc.xds_fallback_timeout_ms",
    "grpc.workaround.cronet_compression",
    "grpc.optimization_target",
    "grpc.enable_retries",
    "grpc.per_rpc_retry_buffer_size",
    "grpc.mobile_log_context",
    "grpc.enable_http_proxy",
    "grpc.surface_user_agent",
    "grpc.inhibit_health_checking",
    "grpc.dns_enable_srv_queries",
    "grpc.dns_ares_query_timeout",
    "grpc.use_local_subchannel_pool",
    "grpc.channel_pooling_domain",
    "grpc.channel_id",
]

Options = typing.Dict[OptionKey, typing.Union[int, float, bool, str, bytes, None]]

class Compression(enum.IntEnum):
    NoCompression = ...
    Deflate = ...
    Gzip = ...


# XXX: not documented, needs more investigation.
# Some evidence:
# - https://github.com/grpc/grpc/blob/0e1984effd7e977ef18f1ad7fde7d10a2a153e1d/src/python/grpcio_tests/tests/unit/_metadata_test.py#L71
# - https://github.com/grpc/grpc/blob/0e1984effd7e977ef18f1ad7fde7d10a2a153e1d/src/python/grpcio_tests/tests/unit/_metadata_test.py#L58
# - https://github.com/grpc/grpc/blob/0e1984effd7e977ef18f1ad7fde7d10a2a153e1d/src/python/grpcio_tests/tests/unit/_invocation_defects_test.py#L66
Metadata = typing.Tuple[
    typing.Tuple[str, typing.Union[str, bytes]],
    ...,
]


"""Create Client"""

def insecure_channel(
    target: str,
    options: typing.Optional[Options] = None,
    compression: typing.Optional[Compression] = None,
) -> Channel:
    ...


def secure_channel(
    target: str,
    credentials: ChannelCredentials,
    options: typing.Optional[Options] = None,
    compression: typing.Optional[Compression] = None,
) -> Channel:
    ...


Interceptor = typing.Union[
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    StreamStreamClientInterceptor,
]

def intercept_channel(channel: Channel, *interceptors: Interceptor) -> Channel:
    ...


"""Create Client Credentials"""

def ssl_channel_credentials(
    root_certificates: typing.Optional[bytes] = None,
    private_key: typing.Optional[bytes] = None,
    certificate_chain: typing.Optional[bytes] = None,
) -> ChannelCredentials:
    ...


def metadata_call_credentials(
    metadata_plugin: AuthMetadataPlugin,
    name: typing.Optional[str] = None,
) -> CallCredentials:
    ...


def access_token_call_credentials(access_token: str) -> CallCredentials:
    ...


# GRPC docs say there should be at least two:
def composite_call_credentials(
    creds1: CallCredentials,
    creds2: CallCredentials,
    *rest: CallCredentials,
) -> CallCredentials:
    ...



# Compose a ChannelCredentials and one or more CallCredentials objects.
def composite_channel_credentials(
    channel_credentials: ChannelCredentials,
    call_credentials: CallCredentials,
    *rest: CallCredentials,
) -> CallCredentials:
    ...
 

"""Create Server"""

def server(
    thread_pool: futures.ThreadPoolExecutor,
    handlers: typing.Optional[typing.List[GenericRpcHandler]] = None,
    interceptors: typing.Optional[typing.List[Interceptor]] = None,
    options: typing.Optional[Options] = None,
    maximum_concurrent_rpcs: typing.Optional[int] = None,
    compression: typing.Optional[Compression] = None,
) -> Server:
    ...


"""Create Server Credentials"""

CertificateChainPair = typing.Tuple[bytes, bytes]

def ssl_server_credentials(
    private_key_certificate_chain_pairs: typing.List[CertificateChainPair],
    root_certificates: typing.Optional[bytes] = None,
    require_client_auth: bool = False,
) -> ServerCredentials:
    ...


def ssl_server_certificate_configuration(
    private_key_certificate_chain_pairs: typing.List[CertificateChainPair],
    root_certificates: typing.Optional[bytes] = None,
) -> ServerCertificateConfiguration:
    ...


def dynamic_ssl_server_credentials(
    initial_certificate_configuration: ServerCertificateConfiguration,
    certificate_configuration_fetcher: typing.Callable[[], ServerCertificateConfiguration],
    require_client_authentication: bool = False,
) -> ServerCredentials:
    ...


"""RPC Method Handlers"""

# XXX: This is probably what appears in the add_FooServicer_to_server function
# in the _pb2_grpc files that get generated, which points to the FooServicer
# handler functions that get generated, which look like this:
#
#    def FloobDoob(self, request, context):
#       return response
#
Behaviour = typing.Callable

# XXX: These are probably the SerializeToTring/FromString pb2 methods, but
# this needs further investigation
RequestDeserializer = typing.Callable
ResponseSerializer = typing.Callable


def unary_unary_rpc_method_handler(
    behavior: Behaviour,
    request_deserializer: typing.Optional[RequestDeserializer] = None,
    response_serializer: typing.Optional[ResponseSerializer] = None,
) -> RpcMethodHandler:
    ...

def unary_stream_rpc_method_handler(
    behavior: Behaviour,
    request_deserializer: typing.Optional[RequestDeserializer] = None,
    response_serializer: typing.Optional[ResponseSerializer] = None,
) -> RpcMethodHandler:
    ...

def stream_unary_rpc_method_handler(
    behavior: Behaviour,
    request_deserializer: typing.Optional[RequestDeserializer] = None,
    response_serializer: typing.Optional[ResponseSerializer] = None,
) -> RpcMethodHandler:
    ...

def stream_stream_rpc_method_handler(
    behavior: Behaviour,
    request_deserializer: typing.Optional[RequestDeserializer] = None,
    response_serializer: typing.Optional[ResponseSerializer] = None,
) -> RpcMethodHandler:
    ...

def method_handlers_generic_handler(
    service: str,
    method_handlers: typing.Dict[str, RpcMethodHandler],
) -> GenericRpcHandler:
    ...


"""Channel Ready Future"""

def channel_ready_future(channel: Channel) -> Future:
    ...


"""Channel Connectivity"""

class ChannelConnectivity(enum.Enum):
    IDLE = ...
    CONNECTING = ...
    READY = ...
    TRANSIENT_FAILURE = ...
    SHUTDOWN = ...



"""gRPC Status Code"""

class Status:
    code: StatusCode

    # XXX: misnamed property, does not align with status.proto, where it is called 'message':
    details: str

    trailing_metadata: Metadata


class StatusCode(enum.Enum):
    OK = ...
    CANCELLED = ...
    UNKNOWN = ...
    INVALID_ARGUMENT = ...
    DEADLINE_EXCEEDED = ...
    NOT_FOUND = ...
    ALREADY_EXISTS = ...
    PERMISSION_DENIED = ...
    UNAUTHENTICATED = ...
    RESOURCE_EXHAUSTED = ...
    FAILED_PRECONDITION = ...
    ABORTED = ...
    UNIMPLEMENTED = ...
    INTERNAL = ...
    UNAVAILABLE = ...
    DATA_LOSS = ...


"""Channel Object"""

# XXX: These are probably the SerializeToTring/FromString pb2 methods, but
# this needs further investigation
RequestSerializer = typing.Callable
ResponseDeserializer = typing.Callable


class Channel:
    def close(self) -> None: ...

    def stream_stream(
        self,
        method: str,
        request_serializer: typing.Optional[RequestSerializer],
        response_deserializer: typing.Optional[ResponseDeserializer],
    ) -> StreamStreamMultiCallable:
        ...

    def stream_unary(
        self,
        method: str,
        request_serializer: typing.Optional[RequestSerializer],
        response_deserializer: typing.Optional[ResponseDeserializer],
    ) -> StreamUnaryMultiCallable:
        ...

    def subscribe(
        self,
        callback: typing.Callable[[ChannelConnectivity], None],
        try_to_connect: bool = False,
    ) -> None:
        ...

    def unary_stream(
        self,
        method: str,
        request_serializer: typing.Optional[RequestSerializer],
        response_deserializer: typing.Optional[ResponseDeserializer],
    ) -> UnaryStreamMultiCallable:
        ...

    def unary_unary(
        self,
        method: str,
        request_serializer: typing.Optional[RequestSerializer],
        response_deserializer: typing.Optional[ResponseDeserializer],
    ) -> UnaryUnaryMultiCallable:
        ...

    def unsubscribe(
        self,
        callback: typing.Callable[[ChannelConnectivity], None],
    ) -> None:
        ...


"""Server Object"""

class Server:
    def add_generic_rpc_handlers(
        self,
        generic_rpc_handlers: typing.Iterable[GenericRpcHandler],
    ) -> None:
        ...

    # Returns an integer port on which server will accept RPC requests.
    def add_insecure_port(self, address: str) -> int:
        ...

    # Returns an integer port on which server will accept RPC requests.
    def add_secure_port(self, address: str, server_credentials: ServerCredentials) -> int:
        ...

    def start(self) -> None:
        ...

    # Grace period is in seconds
    def stop(self, grace: typing.Optional[int] = None) -> threading.Event:
        ...


"""Authentication & Authorization Objects"""

class ChannelCredentials:
    """This class has no supported interface"""


class CallCredentials:
    """This class has no supported interface"""


class AuthMetadataContext:
    service_url: str
    method_name: str


class AuthMetadataPluginCallback:
    def __call__(self, metadata: Metadata, error: typing.Optional[Exception]) -> None:
        ...


class AuthMetadataPlugin:
    def __call__(self, context: AuthMetadataContext, callback: AuthMetadataPluginCallback) -> None:
        ...


class ServerCredentials:
    """This class has no supported interface"""


class ServerCertificateConfiguration:
    """This class has no supported interface"""


"""gRPC Exceptions"""

class _Metadatum:
    key: str
    value: bytes


class RpcError(Exception):
    def code(self) -> StatusCode: ...

    # misnamed property, does not align with status.proto, where it is called 'message':
    def details(self) -> str: ...

    # XXX: This has a slightly different return type to all the other metadata:
    def trailing_metadata(self) -> typing.Tuple[_Metadatum, ...]: ...


"""Shared Context"""

class RpcContext:
    def add_callback(self, callback: typing.Callable[[], None]) -> bool: ...
    def cancel(self) -> None: ...
    def is_active(self) -> bool: ...
    def time_remaining(self) -> float: ...


"""Client-Side Context"""

class Call:
    def code(self) -> StatusCode: ...

    # misnamed property, does not align with status.proto, where it is called 'message':
    def details(self) -> str: ...

    def initial_metadata(self) -> Metadata: ...
    def trailing_metadata(self) -> Metadata: ...


"""Client-Side Interceptor"""

class ClientCallDetails:
    method: str
    timeout: float
    metadata: Metadata

    # FIXME: unsure if Optional is appropriate, but 'optional' is present in the docs
    credentials: typing.Optional[CallCredentials]

    # FIXME: Unsure from the docs what the precise shape is
    # "This is an EXPERIMENTAL argument. An optional flag t enable wait for ready mechanism."
    wait_for_ready: bool

    compression: Compression


TRequest = typing.TypeVar("TRequest")
TResponse = typing.TypeVar("TResponse")

# An object that is both a Call for the RPC and a Future. In the event of
# RPC completion, the return Call-Future’s result value will be the
# response message of the RPC. Should the event terminate with non-OK
# status, the returned Call-Future’s exception value will be an RpcError.
#
class CallFuture(typing.Generic[TResponse], Call, Future[TResponse]):
    pass


class UnaryUnaryClientInterceptor(typing.Generic[TRequest, TResponse]):
    def intercept_unary_unary(
        self,

        # FIXME: decode these cryptic runes to confirm the typing mystery of
        # this callable's signature that was left for us by past civilisations:
        #
        #     continuation – A function that proceeds with the invocation by
        #     executing the next interceptor in chain or invoking the actual RPC
        #     on the underlying Channel. It is the interceptor’s responsibility
        #     to call it if it decides to move the RPC forward. The interceptor
        #     can use response_future = continuation(client_call_details,
        #     request) to continue with the RPC. continuation returns an object
        #     that is both a Call for the RPC and a Future. In the event of RPC
        #     completion, the return Call-Future’s result value will be the
        #     response message of the RPC. Should the event terminate with non-OK
        #     status, the returned Call-Future’s exception value will be an
        #     RpcError.
        #
        continuation: typing.Callable[[ClientCallDetails, TRequest], CallFuture[TResponse]],

        client_call_details: ClientCallDetails,

        request: TRequest,

    ) -> CallFuture[TResponse]:
        ...


class CallIterator(typing.Generic[TResponse], Call):
    def __iter__(self) -> typing.Iterable[TResponse]: ...


class UnaryStreamClientInterceptor(typing.Generic[TRequest, TResponse]):
    def intercept_unary_stream(
        self,
        continuation: typing.Callable[[ClientCallDetails, TRequest], CallIterator[TResponse]],
        client_call_details: ClientCallDetails,
        request: TRequest,
    ) -> CallIterator[TResponse]:
        ...


class StreamUnaryClientInterceptor(typing.Generic[TRequest, TResponse]):
    def intercept_stream_unary(
        self,
        continuation: typing.Callable[[ClientCallDetails, TRequest], CallFuture[TResponse]],
        client_call_details: ClientCallDetails,
        request_iterator: typing.Iterable[TRequest],
    ) -> CallFuture[TResponse]:
        ...


class StreamStreamClientInterceptor(typing.Generic[TRequest, TResponse]):
    def intercept_stream_stream(
        self,
        continuation: typing.Callable[[ClientCallDetails, TRequest], CallIterator[TResponse]],
        client_call_details: ClientCallDetails,
        request_iterator: typing.Iterable[TRequest],
    ) -> CallIterator[TResponse]:
        ...


"""Service-Side Context"""

class ServicerContext:

    # misnamed parameter 'details', does not align with status.proto, where it is called 'message':
    def abort(self, code: StatusCode, details: str) -> None: ...
    def abort_with_status(self, status: Status) -> None: ...

    # FIXME: The docs say "A map of strings to an iterable of bytes for each auth property".
    # Does that mean 'bytes' (which is iterable), or 'typing.Iterable[bytes]'?
    def auth_context(self) -> typing.Mapping[str, bytes]:
        ...

    def disable_next_message_compression(self) -> None: ...

    def invocation_metadata(self) -> Metadata: ...

    def peer(self) -> str: ...
    def peer_identities(self) -> typing.Optional[typing.Iterable[bytes]]: ...
    def peer_identity_key(self) -> typing.Optional[str]: ...
    def send_initial_metadata(self, initial_metadata: Metadata) -> None: ...
    def set_code(self, code: StatusCode) -> None: ...
    def set_compression(self, compression: Compression) -> None: ...
    def set_trailing_metadata(self, trailing_metadata: Metadata) -> None: ...

    # misnamed function 'details', does not align with status.proto, where it is called 'message':
    def set_details(self, details: str) -> None: ...


"""Service-Side Handler"""

class RpcMethodHandler(typing.Generic[TRequest, TResponse]):
    request_streaming: bool
    response_streaming: bool

    # XXX: not clear from docs whether this is optional or not
    request_deserializer: typing.Optional[RequestDeserializer]

    # XXX: not clear from docs whether this is optional or not
    response_serializer: typing.Optional[ResponseSerializer]

    unary_unary: typing.Optional[typing.Callable[[TRequest, ServicerContext], TResponse]]

    unary_stream: typing.Optional[typing.Callable[[TRequest, ServicerContext], typing.Iterable[TResponse]]]

    stream_unary: typing.Optional[typing.Callable[[typing.Iterable[TRequest], ServicerContext], TResponse]]

    stream_stream: typing.Optional[typing.Callable[[typing.Iterable[TRequest], ServicerContext], typing.Iterable[TResponse]]]


class HandlerCallDetails:
    method_name: str
    invocation_metadata: Metadata


class GenericRpcHandler(typing.Generic[TRequest, TResponse]):
    def service(self, handler_call_details: HandlerCallDetails) -> typing.Optional[RpcMethodHandler[TRequest, TResponse]]:
        ...

class ServiceRpcHandler:
    def service_name(self) -> str: ...


"""Service-Side Interceptor"""

class ServerInterceptor(typing.Generic[TRequest, TResponse]):
    def intercept_service(
        self,
        continuation: typing.Callable[
            [HandlerCallDetails], 
            typing.Optional[RpcMethodHandler[TRequest, TResponse]]
        ],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler[TRequest, TResponse]:
        ...


"""Multi-Callable Interfaces"""

class UnaryUnaryMultiCallable(typing.Generic[TRequest, TResponse]):
    def __call__(
        self,
        request: TRequest,
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,
    ) -> TResponse:
        ...

    def future(
        self,
        request: TRequest,
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,
    ) -> CallFuture[TResponse]:
        ...

    def with_call(
        self,
        request: TRequest,
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,

    # FIXME: Return value is documented as "The response value for the RPC and a Call value for the RPC";
    # this is slightly unclear so this return type is a best-effort guess.
    ) -> typing.Tuple[TResponse, Call]:
        ...


class UnaryStreamMultiCallable(typing.Generic[TRequest, TResponse]):
    def __call__(
        self,
        request: TRequest,
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,

    ) -> CallIterator[TResponse]:
        ...


class StreamUnaryMultiCallable(typing.Generic[TRequest, TResponse]):
    def __call__(
        self,
        request_iterator: typing.Iterable[TRequest],
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,
    ) -> TResponse:
        ...

    def future(
        self,
        request_iterator: typing.Iterable[TRequest],
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,
    ) -> CallFuture[TResponse]:
        ...

    def with_call(
        self,
        request_iterator: typing.Iterable[TRequest],
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,

    # FIXME: Return value is documented as "The response value for the RPC and a Call value for the RPC";
    # this is slightly unclear so this return type is a best-effort guess.
    ) -> typing.Tuple[TResponse, Call]:
        ...


class StreamStreamMultiCallable(typing.Generic[TRequest, TResponse]):
    def __call__(
        self,
        request_iterator: typing.Iterable[TRequest],
        timeout: typing.Optional[int] = None,
        metadata: typing.Optional[Metadata] = None,
        credentials: typing.Optional[CallCredentials] = None,

        # FIXME: optional bool seems weird, but that's what the docs suggest
        wait_for_ready: typing.Optional[bool] = None,

        compression: typing.Optional[Compression] = None,

    ) -> CallIterator[TResponse]:
        ...


"""Future Interfaces"""


class FutureTimeoutError(Exception):
    pass


class FutureCancelledError(Exception):
    pass


TFutureValue = typing.TypeVar("TFutureValue")

class Future(typing.Generic[TFutureValue]):
    def add_done_callback(self, fn: typing.Callable[[Future[TFutureValue]], None]) -> None:
        ...

    def cancel(self) -> bool: ...
    def cancelled(self) -> bool: ...
    def done(self) -> bool: ...
    def exception(self) -> typing.Optional[Exception]: ...
    def result(self, timeout: typing.Optional[float] = None) -> TFutureValue: ...
    def running(self) -> bool: ...

    # FIXME: unsure of the exact return type here. Is it a traceback.StackSummary?
    def traceback(self, timeout: typing.Optional[float] = None) -> typing.Any: ...

