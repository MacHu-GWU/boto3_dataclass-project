# -*- coding: utf-8 -*-

"""
Base class for all generated dataclasses.
"""

from typing import Generic, TypeVar, Self
import dataclasses

T_MODEL = TypeVar("T_MODEL")


@dataclasses.dataclass(frozen=True)
class Base(Generic[T_MODEL]):
    _data: T_MODEL = dataclasses.field()

    @classmethod
    def new(cls, data: T_MODEL):
        return cls(_data=data)

    @property
    def raw_data(self) -> T_MODEL:
        return self._data


if __name__ == "__main__":
    from typing import TypedDict
    from functools import cached_property

    class UserModel(TypedDict):
        special_user_attr: int

    @dataclasses.dataclass(frozen=True)
    class User(Base["UserModel"]):
        @cached_property
        def special_user_attr(self):
            return self._data["special_user_attr"]

    user = User.new({"special_user_attr": 123})

    print(f"{user.raw_data = }")
    print(f"{user.special_user_attr = }")

