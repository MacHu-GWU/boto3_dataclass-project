# -*- coding: utf-8 -*-

import dataclasses

from ..templates.template_enum import tpl_enum
from ..structures.service import Service


@dataclasses.dataclass
class Package:
    """
    Represents a generated boto3 dataclass package for a specific AWS service and version.
    """

    service: Service
    version: str

    def gen_code_pyproject_toml(self):
        return tpl_enum.boto3_dataclass_service__pyproject_toml.render(package=self)

    def gen_code_init_py(self):
        return tpl_enum.boto3_dataclass_service__package____init___py.render(
            package=self
        )

    # def write_type_defs_py(self):
    #     path = self.service.path_boto3_dataclass_type_defs_py
    #     # TODO


# path = self.service.path_boto3_dataclass_pyproject_toml
# write(path, s)

# path = self.service.path_boto3_dataclass_init_py
# write(path, s)
