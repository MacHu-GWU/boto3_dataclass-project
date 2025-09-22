# -*- coding: utf-8 -*-

"""
- 不要对 NotRequired 和 Required 进行特殊处理, 不要用 get() 方法获得 None, 它跟
    Optional 的含义是不同的. 如果尝试获得一个 NotRequired 的属性, 那么就该抛出 KeyError 异常.
- 对于 Optional, 因为说明这个 field 必须存在, 但是值可以是 None, 所以直接访问即可.
"""

from typing import TYPE_CHECKING, List, Dict
import dataclasses
from functools import cached_property

from boto3_dataclass.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from boto3_dataclass.tests.gen_code import type_defs


@dataclasses.dataclass(frozen=True)
class SimpleModel(Base["type_defs.SimpleModelTypeDef"]):
    @cached_property
    def attr1(self):
        return self._data["attr1"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithSubscript(Base["type_defs.SimpleModelWithSubscriptTypeDef"]):
    @cached_property
    def attr1(self):
        return self._data["attr1"]

    @cached_property
    def attr2(self):
        return self._data["attr2"]

    @cached_property
    def attr3(self):
        return self._data["attr3"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithNestedSubscript(Base["type_defs.SimpleModelWithNestedSubscriptTypeDef"]):
    @cached_property
    def attr1(self):
        return self._data["attr1"]

    @cached_property
    def attr2(self):
        return self._data["attr2"]


@dataclasses.dataclass(frozen=True)
class SimpleContainer(Base["type_defs.SimpleContainerTypeDef"]):
    @cached_property
    def attr1(self):
        return SimpleModel.make_one(self._data["attr1"])

    @cached_property
    def attr2(self):
        return SimpleModel.make_one(self._data["attr2"])

    @cached_property
    def attr3(self):
        return SimpleModel.make_one(self._data["attr3"])

    @cached_property
    def attr4(self):
        return SimpleModel.make_one(self._data["attr4"])

    @cached_property
    def attr5(self):
        return SimpleModel.make_one(self._data["attr5"])

    @cached_property
    def attr6(self):
        return SimpleModel.make_one(self._data["attr6"])

    @cached_property
    def attr7(self):
        return [SimpleModel.make_one(data) for data in self._data["attr7"]]

    @cached_property
    def attr8(self):
        return [SimpleModel.make_one(data) for data in self._data["attr8"]]


# class SimpleContainerTypeDef(TypedDict):
#     attr1: SimpleModelTypeDef
#     attr2: Optional[SimpleModelTypeDef]
#     attr3: Required[SimpleModelTypeDef]
#     attr4: NotRequired[SimpleModelTypeDef]
#     attr5: Required[Optional[SimpleModelTypeDef]]
#     attr6: Required[List[SimpleModelTypeDef]]
#     attr7: NotRequired[List[SimpleModelTypeDef]]

# @dataclasses.dataclass(frozen=True)
# class Profile(Base["type_defs.ProfileTypeDef"]):
#
#     @cached_property
#     def firstname(self):
#         return self._data["firstname"]
#
#     @cached_property
#     def lastname(self):
#         return self._data["lastname"]
#
#     @cached_property
#     def phone_number(self):
#         return self._data.get("phone_number")
#
#     @cached_property
#     def status(self):
#         return self._data["status"]
#
#
# @dataclasses.dataclass(frozen=True)
# class User(Base["type_defs.UserTypeDef"]):
#
#     @cached_property
#     def user_id(self):
#         return self._data["user_id"]
#
#     @cached_property
#     def profile(self):
#         return Profile.new(self._data["profile"])
#
#     @cached_property
#     def labels(self):
#         return self._data.get("labels", [])
#
#     @cached_property
#     def tags(self):
#         return self._data["tags"]
