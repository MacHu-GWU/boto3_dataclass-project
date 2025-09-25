# -*- coding: utf-8 -*-

"""
我们访问 boto3_raw_data 中的字段时, 为了提供 auto complete, 我们用 @cached_property
来包装一个方法, 代码如下::

    @cached_property
    def profile(self):
        return self.boto3_raw_data["profile"]

我们如果能将其简化为类似于下面这样的代码, 由于我们的大部分代码都是自动生成的, 这样做可以大幅
减少代码量::

    profile = field("profile")
"""

import typing as T
import dataclasses
from functools import cached_property


class Profile:
    def profile_method(self):
        pass


class UserTypeDef(T.TypedDict):
    profile: Profile


@dataclasses.dataclass
class User1:
    boto3_raw_data: "UserTypeDef" = dataclasses.field()

    @cached_property
    def profile(self):
        return self.boto3_raw_data["profile"]


user1 = User1(boto3_raw_data={"profile": Profile()})
user1.profile.profile_method()  # type hint work and is valid


def field(name: str):
    """创建一个 cached_property，从 boto3_raw_data 中提取指定字段"""

    def getter(self):
        return self.boto3_raw_data[name]

    return cached_property(getter)


@dataclasses.dataclass
class User2:
    boto3_raw_data: "UserTypeDef" = dataclasses.field()

    profile = field("profile")


user2 = User1(boto3_raw_data={"profile": Profile()})
user2.profile.profile_method()  # type hint work and is valid
