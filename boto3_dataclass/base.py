# -*- coding: utf-8 -*-

"""
Base class for all generated dataclasses.
"""

from typing import Generic, TypeVar, Iterable, Union, List, Self
import dataclasses

T_MODEL = TypeVar("T_MODEL")


@dataclasses.dataclass(frozen=True)
class Base(Generic[T_MODEL]):
    _data: T_MODEL = dataclasses.field()

    @classmethod
    def make_one(cls, data: T_MODEL | None):
        if data is None:
            return None
        return cls(_data=data)

    # @classmethod
    # def make_many(cls, data: Iterable[T_MODEL]):
    #     return [cls(_data=dct) for dct in data]

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

        def user_method(self):
            pass

    user = User.make_one({"special_user_attr": 123})
    print(f"{user.raw_data = }")
    print(f"{user.special_user_attr = }")
    _ = user.user_method()  # type hint works

    # users = User.make_many([{"special_user_attr": 123}])
    # user = users[0]
    # print(f"{user.raw_data = }")
    # print(f"{user.special_user_attr = }")
    # _ = user.user_method()  # type hint NOT work
