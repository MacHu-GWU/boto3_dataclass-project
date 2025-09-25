# -*- coding: utf-8 -*-

"""
这个模块展示了 boto3-stubs 的 type_defs.pyi 文件中出现过的类型定义模式.
我们的 Parser 也就只需要处理这些模式既可.
"""

from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Mapping,
    Sequence,
    TypedDict,
    Required,
    NotRequired,
    Any,
)

if TYPE_CHECKING:  # pragma: no cover
    import mypy_boto3_ec2.type_defs
    import mypy_boto3_s3.type_defs
    import mypy_boto3_lambda.type_defs


class Model01TypeDef(TypedDict):
    attr_01: str
    attr_02: Required[str]
    attr_03: NotRequired[str]
    attr_11: List[str]
    attr_12: Dict[str, Any]
    attr_13: Sequence[str]
    attr_14: Mapping[str, str]
    attr_21: Required[List[str]]
    attr_22: Required[Dict[str, Any]]
    attr_23: Required[Sequence[str]]
    attr_24: Required[Mapping[str, str]]
    attr_25: NotRequired[List[str]]
    attr_26: NotRequired[Dict[str, Any]]
    attr_27: NotRequired[Sequence[str]]
    attr_28: NotRequired[Mapping[str, str]]


Model02TypeDef = TypedDict(
    "Model02TypeDef",
    {
        "attr_01": str,
        "attr_02": Required[str],
        "attr_03": NotRequired[str],
        "attr_11": List[str],
        "attr_12": Dict[str, Any],
        "attr_13": Sequence[str],
        "attr_14": Mapping[str, str],
        "attr_21": Required[List[str]],
        "attr_22": Required[Dict[str, Any]],
        "attr_23": Required[Sequence[str]],
        "attr_24": Required[Mapping[str, str]],
        "attr_25": NotRequired[List[str]],
        "attr_26": NotRequired[Dict[str, Any]],
        "attr_27": NotRequired[Sequence[str]],
        "attr_28": NotRequired[Mapping[str, str]],
    },
)
