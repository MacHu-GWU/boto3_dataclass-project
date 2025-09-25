# -*- coding: utf-8 -*-

import dataclasses

from .._version import __version__
from ..templates.api import tpl_enum
from ..structures.api import PyProjectStructure, Boto3DataclassServiceStructure

from .publish_pyproject import PyProjectBuilder


def gen_code_pyproject_toml(self):
    return tpl_enum.boto3_dataclass__pyproject_toml.render(package=self)


def gen_code_init_py(self):
    return tpl_enum.boto3_dataclass__package____init___py.render(package=self)


@dataclasses.dataclass
class Boto3DataclassBuilder(PyProjectBuilder):
    structure: "PyProjectStructure" = dataclasses.field()
    service_names: list[str] = dataclasses.field(default_factory=list)

    @classmethod
    def new(
        cls,
        version: str = __version__,
        package_name: str = "boto3_dataclass",
    ):
        structure_list = Boto3DataclassServiceStructure.list_all()
        service_names = [struct.service_name for struct in structure_list]
        return cls(
            version=version,
            structure=PyProjectStructure(package_name=package_name),
            service_names=service_names,
        )

    def log(self, ith: int | None = None):
        path = f"file://{self.structure.dir_repo}"
        print(f"========== Work on {self.structure.package_name}: {path}")

    def build_all(self):
        self.structure.remove_dir()
        self.build_init_py()
        self.build_pyproject_toml()
        self.build_README_rst()
        self.build_LICENSE_txt()

    def build_init_py(self):
        path = self.structure.path_init_py
        tpl = tpl_enum.boto3_dataclass__package____init___py
        self.build_by_template(path, tpl)

    def build_pyproject_toml(self):
        path = self.structure.path_pyproject_toml
        tpl = tpl_enum.boto3_dataclass__pyproject_toml
        self.build_by_template(path, tpl)

    def build_README_rst(self):
        path = self.structure.path_README_rst
        tpl = tpl_enum.boto3_dataclass__README_rst
        self.build_by_template(path, tpl)

    def build_LICENSE_txt(self):
        path = self.structure.path_LICENSE_txt
        tpl = tpl_enum.common__LICENSE_txt
        self.build_by_template(path, tpl)
