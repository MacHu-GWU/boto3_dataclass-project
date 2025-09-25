# -*- coding: utf-8 -*-

import shutil
import subprocess
import dataclasses
from functools import cached_property

import mpire
from black import format_file_contents, Mode
import twine.settings
import twine.commands.upload
from twine.exceptions import TwineException
from ..vendor.better_pathlib import temp_cwd

from ..utils import write, SemVer
from ..paths import path_enum
from ..config import config
from ..templates.api import tpl_enum
from ..structures.api import Service
from ..parsers.api import TypedDefsModuleParser
from ..parsers.api import ClientModuleParser


def black_format_code(code: str) -> str:
    return format_file_contents(code, fast=True, mode=Mode())


def gen_code_pyproject_toml(self):
    return tpl_enum.boto3_dataclass_service__pyproject_toml.render(package=self)


def gen_code_init_py(self):
    return tpl_enum.boto3_dataclass_service__package____init___py.render(package=self)


@dataclasses.dataclass
class PackageBuilder:
    service: Service = dataclasses.field()
    version: str = dataclasses.field()

    @cached_property
    def sem_ver(self) -> SemVer:
        return SemVer.parse(self.version)

    def log(self, ith: int | None = None):
        path = f"file://{self.service.dir_boto3_dataclass_repo}"
        if ith:
            seq = f"{ith} "
        else:
            seq = ""
        print(f"========== Work on {seq}{self.service.service_name}: {path}")

    def setup(self):
        shutil.rmtree(self.service.dir_boto3_dataclass_repo, ignore_errors=True)

    def build_all(self):
        self.setup()
        self.build_type_defs()
        self.build_caster()
        self.build_init_py()
        self.build_pyproject_toml()
        self.build_README_rst()
        self.build_LICENSE_txt()

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
        code = black_format_code(code)
        # Write to file
        write(path, code)

    def build_caster(self):
        path_stub_file = self.service.path_mypy_boto3_client_pyi
        cm_parser = ClientModuleParser(path_stub_file=path_stub_file)
        cm = cm_parser.parse()
        path = self.service.path_boto3_dataclass_caster_py
        code = cm.gen_code()
        # Format code with black
        code = black_format_code(code)
        # Write to file
        write(path, code)

    def _build_by_package(
        self,
        path,
        template,
    ):
        code = template.render(package=self)
        write(path, code)

    def build_init_py(self):
        path = self.service.path_boto3_dataclass_init_py
        tpl = tpl_enum.boto3_dataclass_service__package____init___py
        self._build_by_package(path, tpl)

    def build_pyproject_toml(self):
        path = self.service.path_boto3_dataclass_pyproject_toml
        tpl = tpl_enum.boto3_dataclass_service__pyproject_toml
        self._build_by_package(path, tpl)

    def build_README_rst(self):
        path = self.service.path_boto3_dataclass_README_rst
        tpl = tpl_enum.boto3_dataclass_service__README_rst
        self._build_by_package(path, tpl)

    def build_LICENSE_txt(self):
        path = self.service.dir_boto3_dataclass_repo / "LICENSE.txt"
        tpl = tpl_enum.boto3_dataclass_service__LICENSE_txt
        self._build_by_package(path, tpl)

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
            package.log(ith)
            package.build_all()

        package_list = cls.list_all(version=version)
        tasks = [
            {"ith": i, "package": package}
            for i, package in enumerate(package_list, start=1)
        ]
        with mpire.WorkerPool(n_jobs=n_workers, start_method="fork") as pool:
            results = pool.map(main, tasks)

    def poetry_build(self):
        args = ["poetry", "build"]
        with temp_cwd(self.service.dir_boto3_dataclass_repo):
            subprocess.run(args)

    def twine_upload(self):
        with temp_cwd(self.service.dir_boto3_dataclass_repo):
            twine.commands.upload.upload(
                upload_settings=config.twine_upload_settings,
                dists=self.service.dist_files,
            )

    def pip_install_editable(self):
        dir_repo = self.service.dir_boto3_dataclass_repo
        args = [
            f"{path_enum.dir_venv_bin / 'pip'}",
            "install",
            "-e",
            ".",
        ]
        with temp_cwd(dir_repo):
            subprocess.run(args)
