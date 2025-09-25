# -*- coding: utf-8 -*-

"""
我最终的决定是, 不要用泛型等任何基类等复杂的设计, 直接每个类都不用继承. 直接用最简单的 Frozen Class.
给每个类都实现这些代码:

- boto3_raw_data: "UserTypeDef" = dataclasses.field()
- make_one
- make_many
"""

import typing as T
import dataclasses
from functools import cached_property

if T.TYPE_CHECKING:  # pragma: no cover

    class UserTypeDef(T.TypedDict):
        special_user_attr: int


@dataclasses.dataclass(frozen=True)
class User:
    boto3_raw_data: "UserTypeDef" = dataclasses.field()

    @classmethod
    def make_one(cls, data: T.Optional["UserTypeDef"]):
        if data is None:
            return None
        return cls(boto3_raw_data=data)

    @classmethod
    def make_many(cls, data: T.Optional[T.Iterable["UserTypeDef"]]):
        if data is None:
            return None
        return [cls(boto3_raw_data=dct) for dct in data]

    @cached_property
    def special_user_attr(self):
        return self.boto3_raw_data["special_user_attr"]

    def user_method(self):
        print("User method called")


data = {"special_user_attr": 123}
# data: "UserTypeDef" = {"special_user_attr": 123}
user = User.make_one(data)
print(f"{user.special_user_attr = }")  # type hint works
user.user_method()  # type hint works
_ = user.boto3_raw_data["special_user_attr"]  # type hint works
# _ = user.boto3_raw_data["invalid_attr"]  # type hint works


data = [
    {"special_user_attr": 123},
]
users = User.make_many(data)
user = users[0]
print(f"{user.special_user_attr = }")  # type hint works
user.user_method()  # type hint works
_ = user.boto3_raw_data["special_user_attr"]  # type hint works
# _ = user.boto3_raw_data["invalid_attr"]  # type hint works
