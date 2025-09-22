# -*- coding: utf-8 -*-

"""
- 不要对 NotRequired 和 Required 进行特殊处理, 不要用 get() 方法获得 None, 它跟
    Optional 的含义是不同的. 如果尝试获得一个 NotRequired 的属性, 那么就该抛出 KeyError 异常.
- 对于 Optional, 因为说明这个 field 必须存在, 但是值可以是 None, 所以直接访问即可.
"""

import typing as T
import dataclasses
from functools import cached_property

if T.TYPE_CHECKING:  # pragma: no cover
    from boto3_dataclass.tests.gen_code import type_defs


@dataclasses.dataclass(frozen=True)
class SimpleModel:
    boto3_raw_data: "type_defs.SimpleModelTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):
        return self.boto3_raw_data["attr1"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithSubscript:
    boto3_raw_data: "type_defs.SimpleModelWithSubscriptTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):
        return self.boto3_raw_data["attr1"]

    @cached_property
    def attr2(self):
        return self.boto3_raw_data["attr2"]

    @cached_property
    def attr3(self):
        return self.boto3_raw_data["attr3"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithNestedSubscript:
    boto3_raw_data: "type_defs.SimpleModelWithNestedSubscriptTypeDef" = (
        dataclasses.field()
    )

    @cached_property
    def attr1(self):
        return self.boto3_raw_data["attr1"]

    @cached_property
    def attr2(self):
        return self.boto3_raw_data["attr2"]


@dataclasses.dataclass(frozen=True)
class SimpleContainer:
    boto3_raw_data: "type_defs.SimpleContainerTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):
        return SimpleModel(boto3_raw_data=self.boto3_raw_data["attr1"])

    @cached_property
    def attr2(self):
        return SimpleModel(boto3_raw_data=self.boto3_raw_data["attr2"])

    @cached_property
    def attr3(self):
        return SimpleModel(boto3_raw_data=self.boto3_raw_data["attr3"])

    @cached_property
    def attr4(self):
        return SimpleModel(boto3_raw_data=self.boto3_raw_data["attr4"])

    @cached_property
    def attr5(self):
        return SimpleModel(boto3_raw_data=self.boto3_raw_data["attr5"])

    @cached_property
    def attr6(self):
        return SimpleModel(boto3_raw_data=self.boto3_raw_data["attr6"])

    @cached_property
    def attr7(self):
        return [
            SimpleModel(boto3_raw_data=data) for data in self.boto3_raw_data["attr7"]
        ]

    @cached_property
    def attr8(self):
        return [
            SimpleModel(boto3_raw_data=data) for data in self.boto3_raw_data["attr8"]
        ]
