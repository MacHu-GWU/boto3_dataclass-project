# -*- coding: utf-8 -*-

"""
由于 Generic[] 对用双引号包裹的类型支持不够好, 所以这次我们不用 Generic.

**结论**:

- 只要 factory classmethod 返回的直接就是 cls(), 他们子类无需重写也能获得正确的类型提示.
- 其他任何情况, 例如 list comprehension, 都需要子类重写 factory classmethod, 否则类型提示会丢失.
"""

from typing import Generic, TypeVar, Iterable, Optional, Union, List, Dict, Any, Self
import dataclasses

T_MODEL = Dict[str, Any]


@dataclasses.dataclass(frozen=True)
class Base:
    _data: T_MODEL = dataclasses.field()

    @classmethod
    def make_one(cls, data: T_MODEL | None):
        if data is None:
            return None
        return cls(_data=data)

    @classmethod
    def _make_many(cls, data: Iterable[T_MODEL] | None):
        if data is None:
            return None
        return [cls(_data=dct) for dct in data]

    @property
    def raw_data(self):
        return self._data


if __name__ == "__main__":
    from typing import TypedDict
    from functools import cached_property

    class UserModel(TypedDict):
        special_user_attr: int

    @dataclasses.dataclass(frozen=True)
    class User(Base):
        _data: UserModel = dataclasses.field()

        @classmethod
        def make_many(cls, data: Iterable[UserModel] | None):
            if data is None:
                return None
            return [cls(_data=dct) for dct in data]

        @cached_property
        def special_user_attr(self):
            return self._data["special_user_attr"]

        def user_method(self):
            pass

    data = {"special_user_attr": 123}
    user = User.make_one(data)
    print(f"{user.raw_data = }")
    print(f"{user.special_user_attr = }")
    _ = user.user_method()  # type hint works
    _ = user.raw_data["special_user_attr"]  # type hint works
    # _ = user.raw_data["invalid_attr"]  # type hint NOT works

    user = User.make_one(None)
    print(f"{user = }")

    data = [
        {"special_user_attr": 123},
    ]
    users = User.make_many(data)

    user = users[0]
    print(f"{user.raw_data = }")
    print(f"{user.special_user_attr = }")
    _ = user.user_method()  # type hint NOT works
    _ = user.raw_data["special_user_attr"]  # type hint NOT works
    # _ = user.raw_data["invalid_attr"]  # type hint NOT works
