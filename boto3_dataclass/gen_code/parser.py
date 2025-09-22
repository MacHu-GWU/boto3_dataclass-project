# -*- coding: utf-8 -*-

import typing as T
import ast
import dataclasses
from pathlib import Path
from functools import cached_property

from rich import print as rprint

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
    def stub_file_content(self) -> str:
        return self.path_stub_file.read_text(encoding="utf-8")

    @property
    def tddm(self) -> TypedDictDefMapping:
        return self._tddm

    @cached_property
    def module(self) -> ast.Module:
        return ast.parse(self.stub_file_content)

    def parse(self) -> TypedDictDefMapping:
        defs = list()
        for i, node_td in enumerate(self.filter_typed_dict_class_def(), start=1):
            # print(f"========== {i}th TypedDict Class Def ==========")
            # print(f"TypedDict Name = {node_td.name}")
            # if node_td.name == "GetFunctionResponseTypeDef":
            if True:
                typed_dict_def = self.parse_typed_dict_class_def(node_td)
                defs.append(typed_dict_def)
                # break
        self._tddm = TypedDictDefMapping(
            defs=defs,
        )
        return self._tddm

    def filter_typed_dict_class_def(self) -> T.Generator[ast.ClassDef, None, None]:
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

    def parse_typed_dict_class_def(
        self,
        node_td: ast.ClassDef,
    ) -> TypedDictDef:
        """
        Parse a TypedDict class definition from an AST node.

        :param node: The AST ClassDef node representing the TypedDict.
            Example, the User part::

            class User(TypedDict):
                id: int
                name: str
        """
        name = node_td.name
        print(f"class {name}: # <--- parse this")
        fields = []
        for i, node in enumerate(node_td.body, start=1):
            # print(f"---------- {i}th TypedDict field ----------")
            if isinstance(node, ast.AnnAssign):
                # print(f"field name = {node.target.id}")
                typed_dict_field = self.parse_typed_dict_ann_assign(node_td, node)
                fields.append(typed_dict_field)
                # break
            else:
                print(f"Not Annotation Assign: {node = }")  # for debug only
        typed_dict_def = TypedDictDef(name=name, fields=fields)
        # rprint(typed_dict_def)
        return typed_dict_def

    def parse_typed_dict_ann_assign(
        self,
        node_td: ast.ClassDef,
        node_attr: ast.AnnAssign,
    ) -> TypedDictField:
        tdf_parser = TypedDictFieldParser(
            source=self.stub_file_content,
            node_td=node_td,
            node_attr=node_attr,
        )
        tdf_parser.parse()
        return tdf_parser.tdf


@dataclasses.dataclass
class TypedDictFieldParser:
    source: str = dataclasses.field()
    node_td: ast.ClassDef = dataclasses.field()
    node_attr: ast.AnnAssign = dataclasses.field()

    tdf: TypedDictField = dataclasses.field(init=False)

    def __post_init__(self):
        self.tdf = TypedDictField(
            name=self.node_attr.target.id,
        )

    def process_type_name(self, type_name: str):
        if type_name.endswith("TypeDef"):
            self.tdf.is_nested_typed_dict = True
            self.tdf.nested_type_name = type_name

    def parse(self):
        text = ast.get_source_segment(self.source, self.node_attr)
        print(f"    {text} # <--- parse this")
        if isinstance(self.node_attr.annotation, ast.Subscript):
            self.handle_subscript(self.node_attr.annotation)
        elif isinstance(self.node_attr.annotation, ast.Name):
            self.handle_name(self.node_attr.annotation)

    def handle_name(self, annotation: ast.Name):
        self.process_type_name(annotation.id)

    def handle_subscript(self, annotation: ast.Subscript):
        subscriptor = annotation.value.id
        # print(f"Subscript type = {subscriptor}")  # for debug only
        if subscriptor in ["Required", "NotRequired"]:
            # print(f'Enter `if subscriptor in ["Required", "NotRequired"]:` branch')
            self.handle_required_not_required_subscript(annotation)
        elif subscriptor == "Optional":
            # print(f'Enter `if subscriptor == "Optional":` branch')
            self.handle_optional_subscript(annotation)
        elif subscriptor == "List":
            # print(f'Enter `if subscriptor == "List":` branch')
            self.handle_list_subscript(annotation)
        elif subscriptor in ["Dict", "Set", "Tuple"]:
            # print(f'Enter `elif subscriptor in ["Dict", "Set", "Tuple"]:` branch')
            pass
        else:
            raise NotImplementedError(f"Unhandled subscriptor: {subscriptor}")

    def handle_required_not_required_subscript(self, annotation: ast.Subscript):
        if isinstance(annotation.slice, ast.Subscript):
            self.handle_subscript(annotation.slice)
        elif isinstance(annotation.slice, ast.Name):
            self.handle_name(annotation.slice)

    def handle_optional_subscript(self, annotation: ast.Subscript):
        if isinstance(annotation.slice, ast.Subscript):
            self.handle_subscript(annotation.slice)
        elif isinstance(annotation.slice, ast.Name):
            self.handle_name(annotation.slice)

    def handle_list_subscript(self, annotation: ast.Subscript):
        self.tdf.nested_type_subscriptor = "List"
        if isinstance(annotation.slice, ast.Subscript):
            self.handle_subscript(annotation.slice)
        elif isinstance(annotation.slice, ast.Name):
            self.handle_name(annotation.slice)


# @dataclasses.dataclass
# class AwsService:
#     """
#     :param name: The name of the AWS Service or module.
#     """
#
#     name: str = dataclasses.field()
#     typed_dict_def_mapping: dict[str, TypedDictDef] = dataclasses.field(
#         default_factory=dict
#     )
#
#     @cached_property
#     def path_type_def_stub_file(self) -> Path:
#         """
#         Get the path to the type definition stub file (type_defs.pyi) for a given package or module name.
#         """
#         folder = f"mypy_boto3_{self.name}"
#         return dir_site_packages.joinpath(folder, "type_defs.pyi")
#
#     @cached_property
#     def module(self) -> ast.Module:
#         print(f"file://{self.path_type_def_stub_file}")
#         return ast.parse(self.path_type_def_stub_file.read_text(encoding="utf-8"))
#
#     def generate_code(self) -> str:
#         for i, node in enumerate(self.module.body, start=1):
#             if isinstance(node, ast.Assign):
#                 # print(f"{node.targets[0].id = }")
#                 # print(f"{node.value = }")
#                 pass
#             elif isinstance(node, ast.ClassDef):
#                 if len(node.bases) and node.bases[0].id == "TypedDict":
#                     if node.name == "GetFunctionResponseTypeDef":
#                         print(f"========== {i} ==========")
#                         print(f"{node.name = }")
#                         self.parse_typed_dict_class_def(node)
#                         break
