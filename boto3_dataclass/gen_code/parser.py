# -*- coding: utf-8 -*-

import typing as T
import ast
import site
import dataclasses
from functools import cached_property
from pathlib import Path
from .gen_code import (
    TypedDictField,
    TypedDictDef,
    TypedDictDefMapping,
)


def parse_ast(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


@dataclasses.dataclass
class Parser:
    path_stub_file: Path = dataclasses.field()
    _tddm: TypedDictDefMapping = dataclasses.field(init=False)

    @cached_property
    def module(self) -> ast.Module:
        return ast.parse(self.path_stub_file.read_text(encoding="utf-8"))

    def parse(self):
        for i, node_td in enumerate(self.iter_typed_dict_class_def(), start=1):
            print(f"========== {i}th TypedDict Class Def ==========")
            print(f"TypedDict Name = {node_td.name}")
            # if node_td.name == "GetFunctionResponseTypeDef":
            if True:
                self.parse_typed_dict_class_def(node_td)
                # break

    def iter_typed_dict_class_def(self) -> T.Generator[ast.ClassDef, None, None]:
        for i, node in enumerate(self.module.body, start=1):
            # print(f"========== {i} ==========")
            # print(f"{node = }")
            if isinstance(node, ast.Assign):
                # print(f"{node.targets[0].id = }")
                # print(f"{node.value = }")
                pass
            elif isinstance(node, ast.ClassDef):
                # print(f"{node.name = }")
                # print(f"{node.bases = }")
                if len(node.bases) and node.bases[0].id == "TypedDict":
                    yield node

    def parse_typed_dict_class_def(self, node_td: ast.ClassDef):
        """
        Parse a TypedDict class definition from an AST node.

        :param node: The AST ClassDef node representing the TypedDict.
            Example, the User part::

            class User(TypedDict):
                id: int
                name: str
        """
        name = node_td.name
        fields = []
        for i, node in enumerate(node_td.body, start=1):
            print(f"---------- {i}th TypedDict field ----------")
            if isinstance(node, ast.AnnAssign):
                print(f"field name = {node.target.id}")
                typed_dict_field = self.parse_typed_dict_ann_assign(node_td, node)
                # break
            else:
                print(f"Not Annotation Assign: {node = }")  # for debug only
        typed_dict_def = TypedDictDef(name=name, fields=fields)
        print(typed_dict_def)
        return typed_dict_def

    def parse_typed_dict_ann_assign(
        self,
        node_td: ast.ClassDef,
        node_attr: ast.AnnAssign,
    ):
        name = node_attr.target.id
        is_nested_typed_dict = False
        nested_type_name = None

        if isinstance(node_attr.annotation, ast.Subscript):
            subscriptor = node_attr.annotation.value.id
            print(f"Subscript type, {subscriptor = }")  # for debug only
            if subscriptor in ["Required", "NotRequired"]:
                if isinstance(node_attr.annotation.slice, ast.Subscript):
                    pass
                else:
                    internal = node_attr.annotation.slice.id
                    if internal.endswith("TypeDef"):
                        is_nested_typed_dict = True
                        nested_type_name = internal
            elif subscriptor == "List":
                internal = node_attr.annotation.slice.id
                print(f"type = List[{internal}]")  # for debug only
                # todo
            elif subscriptor in ["Dict", "Set", "Tuple"]:
                pass

            # print(f"{node_attr.annotation.slice.id = }")
            pass
        elif isinstance(node_attr.annotation, ast.Name):
            type_name = node_attr.annotation.id
            print(f"Simple type, type name = {type_name}")
            # if type_name.endswith("TypeDef"):
            #     is_nested_typed_dict = True
            #     nested_type_name = type_name
            #     print(f"{node_attr.annotation.id = }")

        typed_dict_field = TypedDictField(
            name=name,
            is_nested_typed_dict=is_nested_typed_dict,
            nested_type_name=nested_type_name,
        )
        print(typed_dict_field)
        return typed_dict_field


@dataclasses.dataclass
class AwsService:
    """
    :param name: The name of the AWS Service or module.
    """

    name: str = dataclasses.field()
    typed_dict_def_mapping: dict[str, TypedDictDef] = dataclasses.field(
        default_factory=dict
    )

    @cached_property
    def path_type_def_stub_file(self) -> Path:
        """
        Get the path to the type definition stub file (type_defs.pyi) for a given package or module name.
        """
        folder = f"mypy_boto3_{self.name}"
        return dir_site_packages.joinpath(folder, "type_defs.pyi")

    @cached_property
    def module(self) -> ast.Module:
        print(f"file://{self.path_type_def_stub_file}")
        return ast.parse(self.path_type_def_stub_file.read_text(encoding="utf-8"))

    def generate_code(self) -> str:
        for i, node in enumerate(self.module.body, start=1):
            if isinstance(node, ast.Assign):
                # print(f"{node.targets[0].id = }")
                # print(f"{node.value = }")
                pass
            elif isinstance(node, ast.ClassDef):
                if len(node.bases) and node.bases[0].id == "TypedDict":
                    if node.name == "GetFunctionResponseTypeDef":
                        print(f"========== {i} ==========")
                        print(f"{node.name = }")
                        self.parse_typed_dict_class_def(node)
                        break
