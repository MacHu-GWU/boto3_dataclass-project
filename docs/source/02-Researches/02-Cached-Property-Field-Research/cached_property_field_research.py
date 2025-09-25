# -*- coding: utf-8 -*-

"""
Cached Property Field Research
==============================================================================


研究背景
------------------------------------------------------------------------------
我们访问 boto3_raw_data 中的字段时, 为了提供 auto complete, 我们用 @cached_property
来包装一个方法, 代码如下::

    @cached_property
    def profile(self):
        return self.boto3_raw_data["profile"]


问题描述
------------------------------------------------------------------------------
由于项目中会根据 TypeHint 生成大量的代码, 每个 cached_property 都对应三行代码。
如果我们能将其简化为类似于下面这样的代码, 可以大幅减少代码量::

    profile = field("profile")


研究成果
------------------------------------------------------------------------------
经过测试, 如果用了 field constructor 而不用 @cached_property,
boto3_dataclass_ec2/type_defs.py 中的代码可以从 84005 行减少到 59538 行,
减少了 24467 行, 约 29.1% 的代码量优化。

这个研究验证了使用 field() 函数可以显著减少生成代码的行数，
同时保持相同的类型提示功能和运行时行为。
"""

import typing as T
import dataclasses
from functools import cached_property


class Profile:
    """示例嵌套对象类，用于测试类型提示功能"""

    def profile_method(self):
        """示例方法，用于验证类型提示是否正常工作"""
        pass


class UserTypeDef(T.TypedDict):
    """用户数据的 TypedDict 定义，模拟 Boto3 API 响应结构"""

    profile: Profile


@dataclasses.dataclass
class User1:
    """使用传统 @cached_property 装饰器的实现方式"""

    boto3_raw_data: "UserTypeDef" = dataclasses.field()

    @cached_property
    def profile(self) -> Profile:
        """通过 cached_property 访问嵌套的 profile 对象

        这是传统的实现方式，需要三行代码：
        1. @cached_property 装饰器
        2. def profile(self): 方法定义
        3. return self.boto3_raw_data["profile"] 返回语句
        """
        return self.boto3_raw_data["profile"]


# 测试传统方式的类型提示功能
user1 = User1(boto3_raw_data={"profile": Profile()})
user1.profile.profile_method()  # 类型提示正常工作且有效


def field(name: str):
    """创建一个 cached_property，从 boto3_raw_data 中提取指定字段

    这个工厂函数将三行 cached_property 代码简化为一行字段赋值，
    大幅减少生成代码的行数。

    Args:
        name: 要从 boto3_raw_data 中提取的字段名

    Returns:
        cached_property: 返回一个 cached_property 对象，
                        用于延迟加载和缓存字段值
    """

    def getter(self):
        """内部 getter 函数，从实例的 boto3_raw_data 中提取字段值"""
        return self.boto3_raw_data[name]

    return cached_property(getter)


@dataclasses.dataclass
class User2:
    """使用优化后的 field() 函数的实现方式"""

    boto3_raw_data: "UserTypeDef" = dataclasses.field()

    # 使用 field() 函数将三行代码简化为一行
    # 这种方式在功能上完全等同于 User1 的 @cached_property 实现
    profile = field("profile")


# 测试优化后方式的类型提示功能
# 注意: 这里应该是 User2 而不是 User1 (原代码中的错误)
user2 = User2(boto3_raw_data={"profile": Profile()})
user2.profile.profile_method()  # 类型提示正常工作且有效
