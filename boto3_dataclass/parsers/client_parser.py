# -*- coding: utf-8 -*-

"""
Parse ``mypy_boto3_${aws_service}/client.pyi`` stub file to extract all client methods

.. note::

    这个模块中的所有 ``*Parser`` 类都使用了 Command Pattern, 也就是虽然是一个类,
    但是它被用来当成一个函数来使用, 主函数只有 ``.parse()`` 这一个. 在整个生命周期内,
    把需要共享的数据作为属性放在 ``_attr_name`` 的属性中, 使得代码更加简洁清晰.
"""

import ast
import dataclasses

from ..constants import BASE_CLIENT, TYPE_DEF
from ..models.caster import CasterMethod, CasterModule

from .base import StubFileParser

# DEBUG = True
DEBUG = False


@dataclasses.dataclass
class ClientModuleParser(StubFileParser):
    """
    从 ``mypy_boto3_${aws_service}/client.pyi`` stub file 中解析出所有 client 方法,
    提取出返回 TypedDict 的方法, 为生成 dataclass 转换器做准备.
    """

    _caster_module: CasterModule = dataclasses.field(init=False)

    @property
    def caster_module(self) -> CasterModule:
        return self._caster_module

    @property
    def service_name(self) -> str:
        return self.path_stub_file.parent.name.removeprefix("mypy_boto3_")

    def parse(self):
        """
        解析 AST 模块, 查找并解析 client 类, 提取所有返回 TypedDict 的方法.
        """
        # 遍历模块的所有顶级节点，寻找 client 类定义
        for i, node in enumerate(self.module.body, start=1):
            if self.is_client_class_node(node):
                self.parse_client_class(node)
                return self.caster_module

        raise ValueError("No client class found in the stub file.")  # pragma: no cover

    def is_client_class_node(self, node) -> bool:
        """
        判断给定的 AST 节点是否是 client 类定义.

        client 类必须继承自 BaseClient.
        """
        if isinstance(node, ast.ClassDef):
            # 基类有且只有一个, 并且是 BaseClient
            if len(node.bases) == 1:
                base = node.bases[0]
                if isinstance(base, ast.Name):
                    if base.id == BASE_CLIENT:
                        return True
        return False

    def parse_client_class(self, node_cd: ast.ClassDef):
        """
        解析 client 类定义, 提取所有返回 TypedDict 的方法.

        :param node_cd: client 类的 AST ClassDef 节点
        """
        name = node_cd.name
        if DEBUG:  # pragma: no cover
            lineno = str(node_cd.lineno).zfill(self.zfill)
            print(f"{lineno} class {name}: # <--- parse this")  # for debug only
        methods = []
        # 遍历类中的所有方法定义
        for i, node in enumerate(node_cd.body, start=1):
            if self.is_client_method_node(node):
                client_method = self.parse_client_method(node)
                methods.append(client_method)
        self._caster_module = CasterModule(
            service_name=self.service_name,
            cms=methods,
        )

    def is_client_method_node(self, node) -> bool:
        """
        判断给定的 AST 节点是否是我们关心的 client 方法.

        我们只关心返回类型是 TypedDict (以 'TypeDef' 结尾) 的方法.
        """
        if isinstance(node, ast.FunctionDef):
            # 检查返回类型注解是否存在且为 Name 类型
            if isinstance(node.returns, ast.Name):
                # 返回类型名必须以 'TypeDef' 结尾
                if node.returns.id.endswith(TYPE_DEF):
                    return True
        return False

    def parse_client_method(self, node: ast.FunctionDef) -> CasterMethod:
        """
        解析 client 方法定义, 提取方法名和返回类型信息.

        :param node: 方法的 AST FunctionDef 节点
        :return: 解析后的 CasterMethod 对象
        """
        method_name = node.name
        return_type = node.returns.id  # boto3-stubs 中的 TypedDict 类型名
        if DEBUG:  # pragma: no cover
            lineno = str(node.lineno).zfill(self.zfill)
            text = f"{lineno}    def {method_name}(self, ...) -> {return_type} # <--- parse this"
            print(text)
        # 创建 CasterMethod 对象，将 boto3-stubs 类型映射到 dataclass 类型
        caster_method = CasterMethod(
            method_name=node.name,
            boto3_stubs_type_name=return_type,
            # 移除 'TypeDef' 后缀得到对应的 dataclass 类型名
            boto3_dataclass_type_name=return_type.removesuffix(TYPE_DEF),
        )
        return caster_method
