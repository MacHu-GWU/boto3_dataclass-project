# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from functools import cached_property

from ..utils import write
from ..templates.template_enum import tpl_enum
from ..structures.service import Service


@dataclasses.dataclass
class Package:
    """
    Represents a generated boto3 dataclass package for a specific AWS service and version.
    """

    service: Service
    version: str

    def write_pyproject_toml(self):
        path = self.service.path_boto3_dataclass_pyproject_toml
        s = tpl_enum.boto3_dataclass_service__pyproject_toml.render(package=self)
        write(path, s)

    def write_init_py(self):
        path = self.service.path_boto3_dataclass_init_py
        s = tpl_enum.boto3_dataclass_service__package____init___py.py.render(
            package=self
        )
        write(path, s)

    def write_type_defs_py(self):
        path = self.service.path_boto3_dataclass_type_defs_py
        # TODO
