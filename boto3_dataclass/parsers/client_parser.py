# -*- coding: utf-8 -*-

import ast
import dataclasses

from ..constants import BASE_CLIENT, TYPE_DEF
from ..models.caster import CasterMethod, CasterModule

from .base import StubFileParser

# DEBUG = True
DEBUG = False


@dataclasses.dataclass
class ClientModuleParser(StubFileParser):
    _caster_module: CasterModule = dataclasses.field(init=False)

    @property
    def caster_module(self) -> CasterModule:
        return self._caster_module

    @property
    def service_name(self) -> str:
        return self.path_stub_file.parent.name.removeprefix("mypy_boto3_")

    def parse(self):
        for i, node in enumerate(self.module.body, start=1):
            if self.is_client_class_node(node):
                self.parse_client_class(node)
                return self.caster_module

        raise ValueError("No client class found in the stub file.")

    def is_client_class_node(self, node) -> bool:
        if isinstance(node, ast.ClassDef):
            # 基类有且只有一个, 并且是 BaseClient
            if len(node.bases) == 1:
                base = node.bases[0]
                if isinstance(base, ast.Name):
                    if base.id == BASE_CLIENT:
                        return True
        return False

    def parse_client_class(self, node_cd: ast.ClassDef):
        name = node_cd.name
        if DEBUG:
            lineno = str(node_cd.lineno).zfill(self.zfill)
            print(f"{lineno} class {name}: # <--- parse this")  # for debug only
        methods = []
        for i, node in enumerate(node_cd.body, start=1):
            if self.is_client_method_node(node):
                client_method = self.parse_client_method(node)
                methods.append(client_method)
        self._caster_module = CasterModule(
            service_name=self.service_name,
            cms=methods,
        )

    def is_client_method_node(self, node) -> bool:
        if isinstance(node, ast.FunctionDef):
            if isinstance(node.returns, ast.Name):
                if node.returns.id.endswith(TYPE_DEF):
                    return True
        return False

    def parse_client_method(self, node: ast.FunctionDef) -> CasterMethod:
        method_name = node.name
        return_type = node.returns.id
        if DEBUG:
            lineno = str(node.lineno).zfill(self.zfill)
            text = f"{lineno}    def {method_name}(self, ...) -> {return_type} # <--- parse this"
            print(text)
        caster_method = CasterMethod(
            method_name=node.name,
            boto3_stubs_type_name=return_type,
            boto3_dataclass_type_name=return_type.removesuffix(TYPE_DEF),
        )
        return caster_method
