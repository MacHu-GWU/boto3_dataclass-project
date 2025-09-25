# -*- coding: utf-8 -*-

from typing import Union, IO, Any, TypedDict
from botocore.response import StreamingBody

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "id": int,
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class PutSnapshotBlockRequestTypeDef(TypedDict):
    BlockData: BlobTypeDef