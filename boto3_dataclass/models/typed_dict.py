# -*- coding: utf-8 -*-

"""
这个模块负责对 TypedDict 这种类型注解进行数据建模. 我们后面的注释会以下面的代码作为例子:

.. code-block:: python

    class UserTypeDef(TypedDict):
        id: Required[int] # <--- 这是一个字段
        name: NotRequired[str] # <--- 这是另一个字段

    class ModelTypeDef(TypedDict):
        attr1: UserTypeDef # <--- 这是一个嵌套 (nested) 的字段
        attr2: Required[UserTypeDef] # <--- 这是一个嵌套的字段
        attr3: NotRequired[UserTypeDef] # <--- 这是一个嵌套的字段
        attr4: Optional[UserTypeDef] # <--- 这是一个嵌套的字段
"""

import typing as T
import dataclasses
from functools import cached_property

from ..constants import TYPE_DEF

from ..templates.template_enum import tpl_enum

# TODO: TypedDictFieldAnnotation.nested_type_subscriptor, 目前只用到了 List 一个, 其他几个到底有没有用还有待观察
NESTED_TYPE_SUBSCRIPTOR = T.Literal[
    "NULL",
    "List",
]


@dataclasses.dataclass
class TypedDictFieldAnnotation:
    """
    储存着 TypedDict 中的一个 field 的类型注解信息. 例如:

    - ``id: int`` 中的 ``int`` 部分, 不包括 ``id``.
    - ``name: Required[str]`` 中的 ``Required[str]`` 部分.

    :param is_nested_typed_dict: 是否是另一个 TypedDict 的类型. 例如
        ``id: str``, ``name: Required[str]`` 这些都不是嵌套的 TypedDict,
        而 ``attr1: UserTypeDef`` 以及 ``attr2, attr3, attr4`` 都是嵌套的 TypedDict.
        这个属性决定了我们在生成 dataclass 的 ``@cached_property`` 的时候, 是直接用
        ``boto3_raw_data.get("field_name")`` 返回一直简单的值, 还是用
        ``User(boto3_raw_data.get("field_name"))`` 返回一个对象.
    :param nested_type_name: 如果是嵌套的 TypedDict 字段, 这里存储着嵌套的 TypedDict 的名称,
        例如 ModelTypeDef 中都是 ``UserTypeDef``. 只有在 is_nested_typed_dict 为 True 的情况下
        才会有值, 否则为 None.
    :param nested_type_subscriptor: 如果是嵌套的 TypedDict 字段, 这里存储着嵌套的 TypedDict 的
        特殊形式. 目前只有 List 这一种特殊形式. 因为在 List 的情况下, ``@cached_property``
        需要用类似于 ``[User(dct) for dct in boto3_raw_data.get("field_name", [])]``
        的形式来生成代码. 而其他的形式, 例如 Required, NotRequired, Optional 都不需要特殊处理.
    """

    is_nested_typed_dict: bool = dataclasses.field(default=False)
    nested_type_name: str | None = dataclasses.field(default=None)
    nested_type_subscriptor: NESTED_TYPE_SUBSCRIPTOR = dataclasses.field(default="NULL")

    @property
    def nested_model_name(self) -> str:
        """
        nested_model 对应的 dataclass 的类名, 例如 ``UserTypeDef`` 对应的就是 ``User``.
        """
        return self.nested_type_name.removesuffix(TYPE_DEF)

field_name_mapping = {
    "lambda": "lambda_",
}

@dataclasses.dataclass
class TypedDictField:
    """
    储存着 TypedDict 的单个字段信息, 例如:

    - UserTypeDef.id
    - UserTypeDef.name

    :param name: 字段名称, 例如 ``id``, ``name``, ``attr1``, ``attr2``, ...
    :param anno: 字段的类型注解信息, 见 :class:`TypedDictFieldAnnotation`.
    """

    name: str = dataclasses.field()
    anno: TypedDictFieldAnnotation = dataclasses.field(
        default_factory=TypedDictFieldAnnotation,
    )

    @property
    def safe_field_name(self) -> str:
        return field_name_mapping.get(self.name, self.name)

    def gen_code(self) -> str:
        """
        生成字段的代码字符串.
        """
        return tpl_enum.boto3_dataclass_service__package__typed_dict_field.render(tdf=self)


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
        """
        通过字段名称获取字段定义的映射, 例如 ``{"id": <TypedDictField>, "name": <TypedDictField>}``.
        """
        return {td.name: td for td in self.fields}

    @property
    def model_name(self) -> str:
        """
        TypedDict 对应的 dataclass 的类名, 例如 ``UserTypeDef`` 对应的就是 ``User``.
        """
        return self.name.removesuffix(TYPE_DEF)

    def gen_code(self) -> str:
        """
        生成 TypedDict 的代码字符串.
        """
        return tpl_enum.boto3_dataclass_service__package__typed_dict_def.render(td=self)


@dataclasses.dataclass
class TypedDefsModule:
    """
    对应一个实现了所有 ``type_defs.pyi`` 文件中的 TypedDict 的 dataclass.
    这个类储存着多个 :class:`TypedDictDef` 的定义信息.
    """

    tdds: list["TypedDictDef"] = dataclasses.field(default_factory=list)

    @cached_property
    def tdds_mapping(self) -> dict[str, "TypedDictDef"]:
        """
        通过 TypedDict 名称获取 TypedDict 定义的映射, 例如 ``{"UserTypeDef": <TypedDictDef>, ...}``.
        """
        return {tdd.name: tdd for tdd in self.tdds}

    def gen_code(self, type_defs_line: str) -> str:
        """
        生成整个模块的代码字符串.

        :param type_defs_line: The line to import the type definitions module.
            Example: ``"from boto3_dataclass.tests.gen_code import type_defs"``
        """
        return tpl_enum.boto3_dataclass_service__package__type_defs_py.render(
            tddm=self, type_defs_line=type_defs_line
        )
