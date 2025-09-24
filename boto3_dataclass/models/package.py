# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from functools import cached_property

from ..paths import path_enum
from ..utils import write
from ..templates.template_enum import tpl_enum


@dataclasses.dataclass
class Package:
    """
    Represents a generated boto3 dataclass package for a specific AWS service and version.
    """

    service: str
    version: str

    @cached_property
    def name(self) -> str:
        mapper = {
            "lambda": "awslambda",
        }
        service = mapper.get(self.service, self.service)
        return f"boto3_dataclass_{service}"

    @cached_property
    def name_slug(self) -> str:
        return self.name.replace("_", "-")

    @cached_property
    def dir_repo(self) -> Path:
        return path_enum.dir_project_root / "build" / "repos" / f"{self.name}-project"

    @cached_property
    def dir_package(self) -> Path:
        return self.dir_repo / self.name

    def write_pyproject_toml(self):
        path = self.dir_repo / "pyproject.toml"
        s = tpl_enum.boto3_dataclass_service__pyproject_toml.render(package=self)
        write(path, s)

    def write_init_py(self):
        path = self.dir_package / "__init__.py"
        s = tpl_enum.boto3_dataclass_service__package____init___py.py.render(
            package=self
        )
        write(path, s)

    def write_type_defs_py(self):
        path = self.dir_package / "type_defs.py"
        # TODO
