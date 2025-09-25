# -*- coding: utf-8 -*-

import shutil
import subprocess
import dataclasses
from pathlib import Path
from functools import cached_property

import twine.commands.upload
from ..vendor.better_pathlib import temp_cwd

from ..paths import path_enum
from ..config import config


@dataclasses.dataclass
class PyProjectStructure:
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

    def remove_dir(self):
        shutil.rmtree(self.dir_repo, ignore_errors=True)

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
        return self.dir_package / "__init__.py"

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

        Example::

            [
                "build/repos/boto3_dataclass_ec2-project/dist/boto3_dataclass_ec2-0.1.1.tar.gz",
                "build/repos/boto3_dataclass_ec2-project/dist/boto3_dataclass_ec2-0.1.1-py3-none-any.whl"
            ]
        """
        dists = list()
        dir_dist = self.dir_repo / "dist"
        for p in dir_dist.iterdir():
            if p.name.startswith(self.package_name) and p.suffix in {".whl", ".tar.gz"}:
                dists.append(str(p))
        return dists

    def poetry_build(self):
        args = ["poetry", "build"]
        with temp_cwd(self.dir_repo):
            subprocess.run(args, check=True)

    def twine_upload(self):
        with temp_cwd(self.dir_repo):
            twine.commands.upload.upload(
                upload_settings=config.twine_upload_settings,
                dists=self.dist_files,
            )

    def pip_install_editable(self):
        args = [
            f"{path_enum.dir_venv_bin / 'pip'}",
            "install",
            "-e",
            ".",
        ]
        with temp_cwd(self.dir_repo):
            subprocess.run(args, check=True)
