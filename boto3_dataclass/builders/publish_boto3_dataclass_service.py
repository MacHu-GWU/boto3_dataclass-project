# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import mpire

from .._version import __version__
from ..utils import black_format_code, write
from ..templates.api import tpl_enum
from ..structures.api import Boto3DataclassServiceStructure
from ..parsers.api import TypedDefsModuleParser
from ..parsers.api import ClientModuleParser

from .publish_pyproject import PyProjectBuilder

if T.TYPE_CHECKING:  # pragma: no cover
    from ..pypi import T_PACKAGE_STATUS_INFO


def gen_code_pyproject_toml(self):
    return tpl_enum.boto3_dataclass_service__pyproject_toml.render(package=self)


def gen_code_init_py(self):
    return tpl_enum.boto3_dataclass_service__package____init___py.render(package=self)


@dataclasses.dataclass
class Boto3DataclassServiceBuilder(PyProjectBuilder):
    structure: "Boto3DataclassServiceStructure" = dataclasses.field()

    def log(self, ith: int | None = None):
        path = f"file://{self.structure.dir_repo}"
        if ith:
            seq = f"{ith} "
        else:
            seq = ""
        print(f"========== Work on {seq}{self.structure.service_name}: {path}")

    def build_all(self):
        self.structure.remove_dir()
        self.build_type_defs()
        self.build_caster()
        self.build_init_py()
        self.build_pyproject_toml()
        self.build_README_rst()
        self.build_LICENSE_txt()

    def build_type_defs(self):
        # Parse mypy_boto3_{service_name}/type_defs.pyi
        path_stub_file = self.structure.path_mypy_boto3_type_defs_pyi
        tdm_parser = TypedDefsModuleParser(path_stub_file=path_stub_file)
        tdm = tdm_parser.parse()
        # Generate boto3_dataclass_{service_name}/type_defs.py
        mypy_package_name = f"mypy_boto3_{self.structure.service_name}"
        type_defs_line = f"from {mypy_package_name} import type_defs"
        path = self.structure.path_boto3_dataclass_type_defs_py
        code = tdm.gen_code(type_defs_line=type_defs_line)
        # Format code with black
        code = black_format_code(code)
        # Write to file
        write(path, code)

    def build_caster(self):
        path_stub_file = self.structure.path_mypy_boto3_client_pyi
        cm_parser = ClientModuleParser(path_stub_file=path_stub_file)
        cm = cm_parser.parse()
        path = self.structure.path_boto3_dataclass_caster_py
        code = cm.gen_code()
        # Format code with black
        code = black_format_code(code)
        # Write to file
        write(path, code)

    def build_init_py(self):
        path = self.structure.path_init_py
        tpl = tpl_enum.boto3_dataclass_service__package____init___py
        self.build_by_template(path, tpl)

    def build_pyproject_toml(self):
        path = self.structure.path_pyproject_toml
        tpl = tpl_enum.boto3_dataclass_service__pyproject_toml
        self.build_by_template(path, tpl)

    def build_README_rst(self):
        path = self.structure.path_README_rst
        tpl = tpl_enum.boto3_dataclass_service__README_rst
        self.build_by_template(path, tpl)

    def build_LICENSE_txt(self):
        path = self.structure.path_LICENSE_txt
        tpl = tpl_enum.common__LICENSE_txt
        self.build_by_template(path, tpl)

    @classmethod
    def list_all(
        cls,
        version: str = __version__,
    ) -> list["Boto3DataclassServiceBuilder"]:
        structure_list = Boto3DataclassServiceStructure.list_all()
        return [
            cls(version=version, structure=structure) for structure in structure_list
        ]

    @classmethod
    def _parallel_run(
        cls,
        func: T.Callable[[int, "Boto3DataclassServiceBuilder"], None],
        version: str = __version__,
        n_workers: int | None = None,
        start_method: str = "fork",
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ):
        if package_status_info is None:
            package_status_info = {}
        package_list = cls.list_all(version=version)
        filtered_package_list = [
            package
            for package in package_list
            if package_status_info.get(package.structure.package_name_slug, False)
            is False
        ]
        sorted_package_list = list(
            sorted(filtered_package_list, key=lambda p: p.structure.package_name_slug)
        )
        if limit is not None:
            sorted_package_list = sorted_package_list[:limit]
        tasks = [
            {"ith": i, "package": package}
            for i, package in enumerate(sorted_package_list, start=1)
        ]
        with mpire.WorkerPool(n_jobs=n_workers, start_method=start_method) as pool:
            results = pool.map(func, tasks)

    @classmethod
    def parallel_build_all(
        cls,
        version: str = __version__,
        n_workers: int | None = None,
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ):
        def main(ith: int, package: "Boto3DataclassServiceBuilder"):
            package.log(ith)
            package.build_all()

        cls._parallel_run(
            version=version,
            func=main,
            n_workers=n_workers,
            start_method="fork",
            package_status_info=package_status_info,
            limit=limit,
        )

    @classmethod
    def parallel_upload_all(
        cls,
        version: str = __version__,
        n_workers: int | None = None,
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ):
        def main(ith: int, package: "Boto3DataclassServiceBuilder"):
            package.log(ith)
            package.structure.poetry_build()
            package.structure.twine_upload()

        cls._parallel_run(
            version=version,
            func=main,
            n_workers=n_workers,
            start_method="threading",
            package_status_info=package_status_info,
            limit=limit,
        )
