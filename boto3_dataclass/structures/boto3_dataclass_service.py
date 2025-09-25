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

from .pyproject import PyProjectStructure

dir_site_packages = Path(site.getsitepackages()[0])


@dataclasses.dataclass
class Boto3DataclassServiceStructure(PyProjectStructure):
    """
    :param name: The name of the AWS Service or module.
    """

    @cached_property
    def service_name(self) -> str:
        return self.package_name.removeprefix("boto3_dataclass_")

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
    def list_all(cls) -> list["Boto3DataclassServiceStructure"]:
        """
        List all available mypy_boto3_* stubs in the site-packages directory.

        :return: A list of Boto3Stubs instances for each discovered service.
        """
        service_list = list()
        for path in dir_site_packages.iterdir():
            if path.name.startswith("mypy_boto3_"):
                if (
                    path.joinpath("client.pyi").exists()
                    and path.joinpath("type_defs.pyi").exists()
                ):
                    service_name = path.name.removeprefix("mypy_boto3_")
                    package_name = f"boto3_dataclass_{service_name}"
                    service_list.append(cls(package_name=package_name))
        return service_list

    @cached_property
    def path_boto3_dataclass_type_defs_py(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/type_defs.py``
        """
        return self.dir_package / "type_defs.py"

    @cached_property
    def path_boto3_dataclass_caster_py(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/caster.py``
        """
        return self.dir_package / "caster.py"
