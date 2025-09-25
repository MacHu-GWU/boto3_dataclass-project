# -*- coding: utf-8 -*-

import ast
import dataclasses
from pathlib import Path
from functools import cached_property


@dataclasses.dataclass
class StubFileParser:
    """
    从 ``mypy_boto3_${aws_service}/*.pyi`` stub file 中解析出结果化的信息

    :param path_stub_file: stub file 的路径.
    """

    path_stub_file: Path = dataclasses.field()

    @cached_property
    def stub_file_content(self) -> str:
        """
        stub file 的内容的字符串形式.
        """
        return self.path_stub_file.read_text(encoding="utf-8")

    @cached_property
    def zfill(self) -> int:
        """
        根据 stub file 的总行数, 计算出行号需要填充多少位数的 0.
        """
        total_lines = len(self.stub_file_content.splitlines())
        return len(str(total_lines))

    @cached_property
    def module(self) -> ast.Module:
        """
        Parse the stub file content into an AST module.
        """
        return ast.parse(self.stub_file_content)
