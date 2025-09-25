# -*- coding: utf-8 -*-

"""
Parse ``mypy_boto3_${aws_service}/type_defs.pyi`` stub file to extract all TypedDict definitions.

.. note::

    这个模块中的所有 ``*Parser`` 类都使用了 Command Pattern, 也就是虽然是一个类,
    但是它被用来当成一个函数来使用, 主函数只有 ``.parse()`` 这一个. 在整个生命周期内,
    把需要共享的数据作为属性放在 ``_attr_name`` 的属性中, 使得代码更加简洁清晰.
"""

import ast
import dataclasses
from pathlib import Path

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass

from ..constants import TYPE_DEF, TYPED_DICT

from ..models.typed_dict import (
    TypedDictFieldAnnotation,
    TypedDictField,
    TypedDictDef,
    TypedDefsModule,
)

from .base import StubFileParser

# DEBUG = True
DEBUG = False


@dataclasses.dataclass
class TypedDefsModuleParser(StubFileParser):
    """
    从 ``mypy_boto3_${aws_service}/type_defs.pyi`` stub file 中解析出所有出现过的
    ``TypedDict`` 的定义.
    """

    _typed_dict_name_set: set[str] = dataclasses.field(default_factory=set)
    _tdm: TypedDefsModule = dataclasses.field(init=False)

    @property
    def tdm(self) -> TypedDefsModule:
        return self._tdm

    def parse(self) -> TypedDefsModule:
        """
        解析 AST 模块, 提取出所有的 TypedDict 定义.
        """
        tdds = list()
        # 遍历模块的所有顶级节点
        # 我们要找两种 TypedDict 定义方式
        for i, node in enumerate(self.module.body, start=1):
            # 第一种是 通过 assign 赋值语句定义的 TypedDict, 类似下面这种
            # UserTypeDef = TypedDict(
            #     "UserTypeDef",
            #     {
            #         "id": int,
            #         "name": str,
            #     },
            # )
            if isinstance(node, ast.Assign):
                # 赋值的等号左边必须有且只有一个目标
                if len(node.targets) != 1:
                    continue
                target = node.targets[0]
                # 赋值的等号左边必须是一个 Name 节点
                if not isinstance(target, ast.Name):
                    continue
                # 变量名必须是以 TypeDef 结尾
                if not target.id.endswith(TYPE_DEF):
                    continue
                # 赋值的等号右边必须是一个 Call 节点 (TypedDict 的工厂函数)
                if not isinstance(node.value, ast.Call):
                    continue
                func = node.value.func
                # 函数名必须是 TypedDict
                if not isinstance(func, ast.Name):
                    continue
                if func.id == TYPED_DICT:
                    self._typed_dict_name_set.add(target.id)
                    typed_dict_def = self.parse_typed_dict_assign(node)
                    # rprint(typed_dict_def)  # for debug only
                    tdds.append(typed_dict_def)
            # 第二种是 通过 class def 定义的 TypedDict, 类似下面这种
            # class UserTypeDef(TypedDict):
            #     id: int
            #     name: str
            elif isinstance(node, ast.ClassDef):
                # 基类有且只有一个, 并且是 TypedDict
                if len(node.bases) == 1 and node.bases[0].id == TYPED_DICT:
                    self._typed_dict_name_set.add(node.name)
                    typed_dict_def = self.parse_typed_dict_class_def(node)
                    # rprint(typed_dict_def)  # for debug only
                    tdds.append(typed_dict_def)
            # 其他类型的节点不是我们关心的.
            else:
                pass
            # break
        self._tdm = TypedDefsModule(
            tdds=tdds,
        )
        return self._tdm

    def parse_typed_dict_assign(
        self,
        node_ass: ast.Assign,
    ) -> TypedDictDef:
        """
        Parse a TypedDict class definition from an AST Assign node.

        :param node_ass: The AST Assign node representing the TypedDict.

            UserTypeDef = TypedDict(
                "UserTypeDef",
                {
                    "id": int,
                    "name": str,
                },
            )
        """
        target: ast.Name = node_ass.targets[0]
        name = target.id
        if DEBUG:
            lineno = str(target.lineno).zfill(self.zfill)
            print(
                f"{lineno} {name} = TypedDict(...) # <--- parse this"
            )  # for debug only
        call: ast.Call = node_ass.value
        # ``kwargs`` is this part
        # {
        #     "id": int,
        #     "name": str,
        # }
        kwargs = call.args[1]  # the {"id"}
        fields = list()
        # For example, in ``"id": int``,
        # ``key`` is the "id" part, ``value`` is the str part
        for key, value in zip(kwargs.keys, kwargs.values):
            if DEBUG:
                key_text = ast.get_source_segment(self.stub_file_content, key)
                value_text = ast.get_source_segment(self.stub_file_content, value)
                text = f"{key_text}: {value_text},"
                lineno = str(key.lineno).zfill(self.zfill)
                print(f"{lineno}    {text} # <--- parse this")  # for debug only
            tdfa_parser = TypedDictFieldAnnotationParser(
                annotation=value,
                _typed_dict_name_set=self._typed_dict_name_set,
            )
            tdfa = tdfa_parser.parse()
            tdf = TypedDictField(
                name=key.value,
                anno=tdfa,
            )
            fields.append(tdf)
            # break
        tdd = TypedDictDef(name=name, fields=fields)
        return tdd

    # --------------------------------------------------------------------------
    # TypedDict
    # --------------------------------------------------------------------------

    def parse_typed_dict_class_def(
        self,
        node_td: ast.ClassDef,
    ) -> TypedDictDef:
        """
        Parse a TypedDict class definition from an AST ClassDef node.

        :param node_td: The AST ClassDef node representing the TypedDict. Example::

            class UserTypeDef(TypedDict):
                id: int
                name: str
        """
        name = node_td.name
        if DEBUG:
            lineno = str(node_td.lineno).zfill(self.zfill)
            print(f"{lineno} class {name}: # <--- parse this")  # for debug only
        fields = []
        for i, node in enumerate(node_td.body, start=1):
            if isinstance(node, ast.AnnAssign):
                if DEBUG:
                    text = ast.get_source_segment(self.stub_file_content, node)
                    lineno = str(node.lineno).zfill(self.zfill)
                    print(f"{lineno}    {text} # <--- parse this")  # for debug only
                typed_dict_field = self.parse_typed_dict_ann_assign(node)
                fields.append(typed_dict_field)
                # break
            else:
                # print(f"Not Annotation Assign: {node = }")  # for debug only
                pass
        typed_dict_def = TypedDictDef(name=name, fields=fields)
        return typed_dict_def

    def parse_typed_dict_ann_assign(
        self,
        node_attr: ast.AnnAssign,
    ) -> TypedDictField:
        tdf_parser = TypedDictFieldParser(
            node_attr=node_attr,
            _typed_dict_name_set=self._typed_dict_name_set,
        )
        tdf = tdf_parser.parse()
        return tdf


@dataclasses.dataclass
class TypedDictFieldAnnotationParser:
    """
    专门用来解析 TypedDict 字段的 field 的类型注解部分.

    例如::

        class User(TypedDict):
            id: int
            name: Required[str]

    在上面这个例子中, 这个类专门用来解析 ``id: int`` 中的 ``int`` 这一部分, 或者
    ``name: Required[str]`` 中的 ``Required[str]`` 这一部分.

    :param is_nested_typed_dict:
    :param nested_type_name:
    :param nested_type_subscriptor:
    """

    annotation: ast.Name | ast.Subscript = dataclasses.field()
    _typed_dict_name_set: set[str] = dataclasses.field(default_factory=set)
    _anno: TypedDictFieldAnnotation = dataclasses.field(init=False)

    @property
    def tdfa(self) -> TypedDictFieldAnnotation:
        return self._anno

    def parse(self) -> TypedDictFieldAnnotation:
        """
        解析类型注解, 只有两种可能:

        1. ast.Name, 类似于 ``a: int``
        2. ast.Subscript, 类似于 ``b: List[int]`` 或者 ``c: Required[str]``
        """
        self._anno = TypedDictFieldAnnotation()
        if isinstance(self.annotation, ast.Name):
            self.handle_name(self.annotation)
        elif isinstance(self.annotation, ast.Subscript):
            self.handle_subscript(self.annotation)
        elif isinstance(self.annotation, (ast.BinOp)):
            pass
        else:
            raise NotImplementedError(f"Unhandled annotation: {self.annotation}")
        return self._anno

    def process_type_name(self, type_name: str):
        """
        处理类型名称, 如果是一个嵌套的 TypedDict, 则标注这个 Field 是一个嵌套的 TypedDict.
        """
        if type_name.endswith(TYPE_DEF):
            if type_name in self._typed_dict_name_set:
                self._anno.is_nested_typed_dict = True
                self._anno.nested_type_name = type_name

    def handle_name(self, annotation: ast.Name):
        """
        处理 ast.Name 类型的注解. 只需要判断是不是嵌套的 TypedDict 就行了.
        """
        self.process_type_name(annotation.id)

    def handle_subscript(self, annotation: ast.Subscript):
        """
        如果是嵌套的 Subscript, 则递归深入处理.
        """
        # 首先确定 value 不分 (括号外) 是一个 Name, 也就是类似于 Required[...]
        # 我们目前无法处理 T.Required[...] 这种情况, 在这种情况下它是一个 ast.Attribute
        if not isinstance(annotation.value, ast.Name):
            raise NotImplementedError(
                f"Unhandled subscript value: {annotation.value}",
            )
        # 然后根据 subscriptor 的不同分情况处理, 其中如果里面的 slice 还是一个 Subscript, 则递归深入处理
        subscriptor = annotation.value.id
        # print(f"Subscript type = {subscriptor}")  # for debug only
        if subscriptor in ["Required", "NotRequired"]:
            self.handle_required_not_required_subscript(annotation)
        elif subscriptor == "Optional":
            self.handle_optional_subscript(annotation)
        # 只要是 List liked, 都当成 List 处理
        elif subscriptor in ["List", "Sequence"]:
            self.handle_list_subscript(annotation)
        elif subscriptor in [
            "Dict",
            "Mapping",
            "Set",
            "Tuple",
            "Literal",
            # Other types we don't handle specially
            "EventStream",
        ]:
            pass
        else:
            raise NotImplementedError(f"Unhandled subscriptor: {subscriptor}")

    def handle_simple_subscript(self, annotation: ast.Subscript):
        if isinstance(annotation.slice, ast.Subscript):
            self.handle_subscript(annotation.slice)
        elif isinstance(annotation.slice, ast.Name):
            self.handle_name(annotation.slice)
        elif isinstance(annotation.slice, (ast.BinOp)):
            pass
        else:
            raise NotImplementedError(f"Unhandled slice: {annotation.slice}")

    def handle_required_not_required_subscript(self, annotation: ast.Subscript):
        self.handle_simple_subscript(annotation)

    def handle_optional_subscript(self, annotation: ast.Subscript):
        self.handle_simple_subscript(annotation)

    def handle_list_subscript(self, annotation: ast.Subscript):
        self._anno.nested_type_subscriptor = "List"
        self.handle_simple_subscript(annotation)


@dataclasses.dataclass
class TypedDictFieldParser:
    """
    专门用来解析 TypedDict 字段的 field.

    例如::

        class User(TypedDict):
            id: int
            name: Required[str]

    在上面这个例子中, 这个类用来解析每一个 ``id: int`` 键值对.

    :param node_attr: ``id: int`` 这一整行的 AST 节点.
    """

    node_attr: ast.AnnAssign = dataclasses.field()

    _typed_dict_name_set: set[str] = dataclasses.field(default_factory=set)
    _tdf: TypedDictField = dataclasses.field(init=False)

    @property
    def tdf(self) -> TypedDictField:
        return self._tdf

    def parse(self) -> TypedDictField:
        tdfa_parser = TypedDictFieldAnnotationParser(
            annotation=self.node_attr.annotation,
            _typed_dict_name_set=self._typed_dict_name_set,
        )
        tdfa = tdfa_parser.parse()
        self._tdf = TypedDictField(
            name=self.node_attr.target.id,
            anno=tdfa,
        )
        return self._tdf
