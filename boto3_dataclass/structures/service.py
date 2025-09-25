# -*- coding: utf-8 -*-

"""
This module defines the Boto3Stubs dataclass for discovering and managing
type definition stub files (type_defs.pyi) for AWS services installed as
mypy_boto3_* packages in the current Python environment.

It provides functionality to:

- Retrieve the path to a type definition stub file for a specific AWS service.
- List all available mypy_boto3_* stubs in the site-packages directory.
"""

import site
import dataclasses
from functools import cached_property
from pathlib import Path

from ..paths import path_enum

# from .type_defs_parser import TypedDictDefMappingParser

dir_site_packages = Path(site.getsitepackages()[0])


service_name_mapping = {
    "lambda": "awslambda",
}


@dataclasses.dataclass
class Service:
    """
    :param name: The name of the AWS Service or module.
    """

    service_name: str = dataclasses.field()

    @cached_property
    def boto3_stubs_package_name(self) -> str:
        return f"mypy_boto3_{self.service_name}"

    @cached_property
    def boto3_stubs_package_name_slug(self) -> str:
        return self.boto3_stubs_package_name.replace("_", "-")

    @cached_property
    def dir_mypy_boto3_package(self) -> Path:
        """
        Get the directory path for a given package or module name.

        Example: ``site-packages/mypy_boto3_ec2``
        """
        return dir_site_packages / self.boto3_stubs_package_name

    @cached_property
    def path_mypy_boto3_literals_pyi(self) -> Path:
        """
        Get the path to the literals stub file (literals.pyi).

        Example: ``site-packages/mypy_boto3_ec2/literals.pyi``
        """
        return self.dir_mypy_boto3_package / "literals.pyi"

    @cached_property
    def path_mypy_boto3_type_defs_pyi(self) -> Path:
        """
        Get the path to the type definition stub file (type_defs.pyi).

        Example: ``site-packages/mypy_boto3_ec2/type_defs.pyi``
        """
        return self.dir_mypy_boto3_package / "type_defs.pyi"

    @cached_property
    def path_mypy_boto3_client_pyi(self) -> Path:
        """
        Get the path to the client stub file (client.pyi).

        Example: ``site-packages/mypy_boto3_ec2/client.pyi``
        """
        return self.dir_mypy_boto3_package / "client.pyi"

    @classmethod
    def list_all(cls) -> list["Service"]:
        """
        List all available mypy_boto3_* stubs in the site-packages directory.

        :return: A list of Boto3Stubs instances for each discovered service.
        """
        service_list = list()
        for path in dir_site_packages.iterdir():
            if path.name.startswith("mypy_boto3_"):
                service_name = path.name.removeprefix("mypy_boto3_")
                service_list.append(cls(service_name=service_name))
        return service_list

    @cached_property
    def boto3_dataclass_package_name(self) -> str:
        """
        Get the corresponding boto3_dataclass package name for the service.

        Example: ``boto3_dataclass_ec2``
        """
        return f"boto3_dataclass_{self.service_name}"

    @cached_property
    def boto3_dataclass_package_name_slug(self) -> str:
        """
        Get the corresponding boto3_dataclass package slug for the service.

        Example: ``boto3-dataclass-ec2``
        """
        return self.boto3_dataclass_package_name.replace("_", "-")

    @cached_property
    def dir_boto3_dataclass_repo(self) -> Path:
        """
        Get the build directory path for the boto3_dataclass package repository.
        We use this directory to publish the package to PyPI.

        Example: ``build/repos/boto3_dataclass_ec2-project``
        """
        return (
            path_enum.dir_project_root
            / "build"
            / "repos"
            / f"{self.boto3_dataclass_package_name}-project"
        )

    @cached_property
    def dir_boto3_dataclass_package(self) -> Path:
        """
        Get the directory path for the boto3_dataclass package.

        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2``
        """
        return self.dir_boto3_dataclass_repo / self.boto3_dataclass_package_name

    @cached_property
    def path_boto3_dataclass_pyproject_toml(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/pyproject.toml``
        """
        return self.dir_boto3_dataclass_repo / "pyproject.toml"

    @cached_property
    def path_boto3_dataclass_README_rst(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/README.rst``
        """
        return self.dir_boto3_dataclass_repo / "README.rst"

    @cached_property
    def path_boto3_dataclass_init_py(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/__init__.py``
        """
        return self.dir_boto3_dataclass_package / "__init__.py"

    @cached_property
    def path_boto3_dataclass_type_defs_py(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/type_defs.py``
        """
        return self.dir_boto3_dataclass_package / "type_defs.py"

    @cached_property
    def path_boto3_dataclass_caster_py(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/caster.py``
        """
        return self.dir_boto3_dataclass_package / "caster.py"

    @cached_property
    def dist_files(self) -> list[str]:
        """
        Get the list of distribution files in the dist directory.

        Example: ``build/repos/boto3_dataclass_ec2-project/dist/boto3_dataclass_ec2-0.1.0-py3-none-any.whl``
        """
        dist_dir = self.dir_boto3_dataclass_repo / "dist"
        return [str(p) for p in dist_dir.iterdir()]
