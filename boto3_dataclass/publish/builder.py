# -*- coding: utf-8 -*-

import shutil
import dataclasses

import mpire
from black import format_file_contents, Mode

from ..utils import write
from ..templates.template_enum import tpl_enum
from ..structures.service import Service
from ..parsers.type_defs_parser import TypedDefsModuleParser


def black_format_code(code: str) -> str:
    return format_file_contents(code, fast=True, mode=Mode())


def gen_code_pyproject_toml(self):
    return tpl_enum.boto3_dataclass_service__pyproject_toml.render(package=self)


def gen_code_init_py(self):
    return tpl_enum.boto3_dataclass_service__package____init___py.render(package=self)


@dataclasses.dataclass
class PackageBuilder:
    service: Service
    version: str

    def setup(self):
        print(f"file://{self.service.dir_boto3_dataclass_repo}")
        shutil.rmtree(self.service.dir_boto3_dataclass_repo, ignore_errors=True)

    def build_all(self):
        self.build_type_defs()
        # self.build_init_py()
        # self.build_pyproject_toml()

    def build_type_defs(self):
        # Parse mypy_boto3_{service_name}/type_defs.pyi
        path_stub_file = self.service.path_mypy_boto3_type_defs_pyi
        tdm_parser = TypedDefsModuleParser(path_stub_file=path_stub_file)
        tdm = tdm_parser.parse()
        # Generate boto3_dataclass_{service_name}/type_defs.py
        mypy_package_name = f"mypy_boto3_{self.service.service_name}"
        type_defs_line = f"from {mypy_package_name} import type_defs"
        path = self.service.path_boto3_dataclass_type_defs_py
        code = tdm.gen_code(type_defs_line=type_defs_line)
        # Format code with black
        # code = black_format_code(code)
        # Write to file
        write(path, code)

    def build_init_py(self):
        path = self.service.path_boto3_dataclass_init_py
        tpl = tpl_enum.boto3_dataclass_service__package____init___py
        code = tpl.render(package=self)
        write(path, code)

    def build_pyproject_toml(self):
        path = self.service.path_boto3_dataclass_pyproject_toml
        tpl = tpl_enum.boto3_dataclass_service__pyproject_toml
        code = tpl.render(package=self)
        write(path, code)

    @classmethod
    def list_all(
        cls,
        version: str,
    ) -> list["PackageBuilder"]:
        service_list = Service.list_all()
        return [cls(service=service, version=version) for service in service_list]

    @classmethod
    def parallel_build_all(
        cls,
        version: str,
        n_workers: int | None = None,
    ):
        def main(ith: int, package: "PackageBuilder"):
            print(f"========== {ith} {package.service.service_name} ==========")
            package.build_all()

        package_list = cls.list_all(version=version)
        tasks = [
            {"ith": i, "package": package}
            for i, package in enumerate(package_list, start=1)
        ]
        with mpire.WorkerPool(n_jobs=n_workers, start_method="fork") as pool:
            results = pool.map(main, tasks)
