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

from ..paths import dir_srv

from .type_defs_parser import TypedDictDefMappingParser

dir_site_packages = Path(site.getsitepackages()[0])


def write(path: Path, text: str):
    try:
        path.write_text(text, encoding="utf-8")
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


@dataclasses.dataclass
class Boto3Stubs:
    """
    :param name: The name of the AWS Service or module.
    """

    service: str = dataclasses.field()

    @cached_property
    def dir_package_folder(self) -> Path:
        """
        Get the directory path for a given package or module name.

        Example: ``site-packages/mypy_boto3_ec2``
        """
        folder = f"mypy_boto3_{self.service}"
        return dir_site_packages / folder

    @cached_property
    def path_literals_stub_file(self) -> Path:
        """
        Get the path to the literals stub file (literals.pyi).

        Example: ``site-packages/mypy_boto3_ec2/literals.pyi``
        """
        return self.dir_package_folder / "literals.pyi"

    @cached_property
    def path_type_def_stub_file(self) -> Path:
        """
        Get the path to the type definition stub file (type_defs.pyi).

        Example: ``site-packages/mypy_boto3_ec2/type_defs.pyi``
        """
        return self.dir_package_folder / "type_defs.pyi"

    @cached_property
    def path_client_stub_file(self) -> Path:
        """
        Get the path to the client stub file (client.pyi).

        Example: ``site-packages/mypy_boto3_ec2/client.pyi``
        """
        return self.dir_package_folder / "client.pyi"

    @classmethod
    def list_all(cls) -> list["Boto3Stubs"]:
        """
        List all available mypy_boto3_* stubs in the site-packages directory.

        :return: A list of Boto3Stubs instances for each discovered service.
        """
        boto3_stubs_list = list()
        for path in dir_site_packages.iterdir():
            if path.name.startswith("mypy_boto3_"):
                service = path.name.removeprefix("mypy_boto3_")
                boto3_stubs_list.append(cls(service=service))
        return boto3_stubs_list

    @cached_property
    def dir_code(self) -> Path:
        """
        Example: ``boto3_dataclass/srv/ec2``
        """
        name = f"{self.service}"
        mapping = {
            "lambda": "lambda_",
        }
        name = mapping.get(name, name)
        return dir_srv / name

    @cached_property
    def path_code_type_defs(self) -> Path:
        """
        Get the path to the generated module file for the service.

        Example: ``boto3_dataclass/srv/ec2/type_defs.py``
        """
        return self.dir_code / "type_defs.py"

    def gen_code(self) -> str:
        tddm_parser = TypedDictDefMappingParser(path_stub_file=self.path_type_def_stub_file)
        tddm = tddm_parser.parse()
        code = tddm.gen_code(
            type_defs_line=f"from mypy_boto3_{self.service} import type_defs",
        )
        return code

    def write_code(self):
        write(self.path_code_type_defs, self.gen_code())
