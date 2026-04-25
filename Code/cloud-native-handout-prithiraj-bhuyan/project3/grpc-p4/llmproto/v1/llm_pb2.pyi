import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompletionRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class LLMStreamRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ("id", "object", "created", "model", "usage", "choices")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    id: str
    object: str
    created: _timestamp_pb2.Timestamp
    model: str
    usage: Usage
    choices: _containers.RepeatedCompositeFieldContainer[Choice]
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., model: _Optional[str] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ..., choices: _Optional[_Iterable[_Union[Choice, _Mapping]]] = ...) -> None: ...

class LLMStreamResponse(_message.Message):
    __slots__ = ("id", "object", "created", "model", "choices")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    id: str
    object: str
    created: _timestamp_pb2.Timestamp
    model: str
    choices: _containers.RepeatedCompositeFieldContainer[Choice]
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., model: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[Choice, _Mapping]]] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ...) -> None: ...

class Choice(_message.Message):
    __slots__ = ("text", "index", "logprobs", "finish_reason")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    text: str
    index: int
    logprobs: str
    finish_reason: str
    def __init__(self, text: _Optional[str] = ..., index: _Optional[int] = ..., logprobs: _Optional[str] = ..., finish_reason: _Optional[str] = ...) -> None: ...
