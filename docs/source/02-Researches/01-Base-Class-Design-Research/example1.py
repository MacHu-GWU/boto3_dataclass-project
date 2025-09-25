# -*- coding: utf-8 -*-

"""
尝试使用 Generic 泛型来标注 Base 类的 _data 属性的类型.

**结论**

- 由于 Generic[] 中间的类是从 stub 文件中导入的, 必须放在 TYPE_CHECKING 保护下,
    所以我们必须用双引号包裹, 这样会导致 Generic 并不能很好的正常工作.
"""

from typing import Generic, TypeVar, Iterable, Optional, Union, List, Dict, Any, Self
import dataclasses

T_MODEL = TypeVar("T_MODEL", bound=Dict[str, Any])


@dataclasses.dataclass(frozen=True)
class Base(Generic[T_MODEL]):
    _data: T_MODEL = dataclasses.field()

    @classmethod
    def make_one(cls, data: T_MODEL | None) -> Self:
        if data is None:
            return None
        return cls(_data=data)

    @property
    def raw_data(self):
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

    data = {"special_user_attr": 123}
    user = User.make_one(data)  # type hint NOT works
    print(f"{user.raw_data = }")
    print(f"{user.special_user_attr = }")
    _ = user.user_method()  # type hint works
    _ = user.raw_data["special_user_attr"]  # type hint works
    # _ = user.raw_data["invalid_attr"]  # type hint NOT works

    user = User.make_one(None)
    print(f"{user = }")
