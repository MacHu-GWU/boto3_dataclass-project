# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from functools import cached_property

from ..paths import path_enum


@dataclasses.dataclass
class PyProject:
    """
    A class representing a Python Project.
    """
    package_name: str = dataclasses.field()

    @cached_property
    def package_name_slug(self) -> str:
        """
        Get the package name in slug format (with hyphens instead of underscores).

        Example:

        - ``boto3-dataclass``
        - ``boto3-dataclass-ec2``
        """
        return self.package_name.replace("_", "-")

    @cached_property
    def dir_repo(self) -> Path:
        """
        Get the build directory path for the boto3_dataclass package repository.
        We use this directory to publish the package to PyPI.

        Example:

        - ``build/repos/boto3_dataclass-project``
        - ``build/repos/boto3_dataclass_ec2-project``
        """
        return (
            path_enum.dir_project_root
            / "build"
            / "repos"
            / f"{self.package_name}-project"
        )

    @cached_property
    def dir_package(self) -> Path:
        """
        Get the directory path for the boto3_dataclass package.

        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2``
        """
        return self.dir_repo / self.package_name

    @cached_property
    def path_init_py(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/__init__.py``
        """
        return self.dir_repo / "__init__.py"

    @cached_property
    def path_pyproject_toml(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/pyproject.toml``
        """
        return self.dir_repo / "pyproject.toml"

    @cached_property
    def path_README_rst(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/README.rst``
        """
        return self.dir_repo / "README.rst"

    @cached_property
    def path_LICENSE_txt(self) -> Path:
        """
        Example: ``build/repos/boto3_dataclass_ec2-project/LICENSE.txt``
        """
        return self.dir_repo / "LICENSE.txt"

    @cached_property
    def dist_files(self) -> list[str]:
        """
        Get the list of distribution files in the dist directory.

        Example: ``build/repos/boto3_dataclass_ec2-project/dist/boto3_dataclass_ec2-0.1.1-py3-none-any.whl``
        """
        dir_dist = self.dir_repo / "dist"
        return [
            str(p) for p in dir_dist.iterdir() if p.name.startswith(self.package_name)
        ]
