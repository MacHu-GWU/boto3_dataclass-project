# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from functools import cached_property

from .template import tpl_enum

# TODO: TypedDictField.nested_type_subscriptor, 目前只用到了 List 一个, 其他几个到底有没有用还有待观察
SubscriptorType = T.Literal[
    "NULL",
    "List",
]


@dataclasses.dataclass
class TypedDictField:
    """
    储存着 TypedDict 的单个字段信息, 例如::

        class UserTypeDef(TypedDict):
            id: Required[int] # <--- 这是一个字段
            name: NotRequired[str] # <--- 这是另一个字段

        class ModelTypeDef(TypedDict):
            attr1: UserTypeDef # <--- 这是一个嵌套的字段
            attr2: Required[UserTypeDef] # <--- 这是一个嵌套的字段
            attr3: NotRequired[UserTypeDef] # <--- 这是一个嵌套的字段
            attr4: Optional[UserTypeDef] # <--- 这是一个嵌套的字段

    :param name: 字段名称, 例如 ``id``, ``name``, ``attr1``, ``attr2``
    :param is_nested_typed_dict: 是否为嵌套的 TypedDict 字段, 例如
        ModelTypeDef 中的 ``attr1``, ``attr2``, ``attr3``, ``attr4``. 换言之,
        这个字段的值我们会用 @cached_property 来缓存一个 dataclass 对象, 而不是字典.
    :param nested_type_name: 如果是嵌套的 TypedDict 字段, 这里存储着嵌套的 TypedDict 的名称,
        例如 ModelTypeDef 中都是 ``UserTypeDef``.
    :param nested_type_subscriptor: 如果是嵌套的 TypedDict 字段, 这里存储着嵌套的 TypedDict 的
        特殊形式, 目前只有 List 这一种特殊形式, 因为在 List 的情况下, 我们需要把 List 里面的每一项都
        转换成 dataclass 对象. 其他的形式, 例如 Required, NotRequired, Optional 都不需要特殊处理.


    """

    name: str = dataclasses.field()
    is_nested_typed_dict: bool = dataclasses.field(default=False)
    nested_type_name: str | None = dataclasses.field(default=None)
    nested_type_subscriptor: SubscriptorType = dataclasses.field(default="NULL")

    @property
    def nested_modeL_name(self) -> str:
        return self.nested_type_name.removesuffix("TypeDef")

    def gen_code(self) -> str:
        return tpl_enum.typed_dict_field.render(tdf=self)


@dataclasses.dataclass
class TypedDictDef:
    """
    储存着 TypedDict 的定义信息, 例如::

        class UserTypeDef(TypedDict):
            id: Required[int]
            name: NotRequired[str]

    :param name: TypedDict 的名称, 例如 ``UserTypeDef``
    :param fields: TypedDict 的字段列表
    """

    name: str = dataclasses.field()
    fields: list["TypedDictField"] = dataclasses.field(default_factory=dict)

    @cached_property
    def fields_mapping(self) -> dict[str, "TypedDictField"]:
        return {td.name: td for td in self.fields}

    @property
    def model_name(self) -> str:
        return self.name.removesuffix("TypeDef")

    def gen_code(self) -> str:
        return tpl_enum.typed_dict_def.render(td=self)


@dataclasses.dataclass
class TypedDictDefMapping:
    """
    储存着多个 TypedDictDef 的定义信息.
    """

    defs: list["TypedDictDef"] = dataclasses.field(default_factory=list)

    @cached_property
    def defs_mapping(self) -> dict[str, "TypedDictDef"]:
        return {tdd.name: tdd for tdd in self.defs}

    def gen_code(self, type_defs_line: str) -> str:
        """
        :param type_defs_line: The line to import the type definitions module.
            Example: ``"from boto3_dataclass.tests.gen_code import type_defs"``
        """
        return tpl_enum.module.render(tddm=self, type_defs_line=type_defs_line)
