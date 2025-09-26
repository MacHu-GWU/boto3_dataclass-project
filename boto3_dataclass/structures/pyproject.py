# -*- coding: utf-8 -*-

"""
Python Project Structure Management.

This module provides the :class:`PyProjectStructure` class that manages the file system structure,
build operations, and distribution management for Python packages in the boto3-dataclass ecosystem.
"""

import shutil
import subprocess
import dataclasses
from pathlib import Path
from functools import cached_property

import requests.exceptions
import twine.commands.upload
from rich import print as rprint
from ..vendor.better_pathlib import temp_cwd

from ..paths import path_enum
from ..config import config

@dataclasses.dataclass
class PyProjectStructure:
    """
    Manages the file system structure and operations for Python projects.

    This class provides a complete abstraction for Python project management,
    including directory structure, build operations, and distribution handling.
    It's designed specifically for boto3-dataclass packages but can be used
    for any Python project following standard conventions.

    The class uses cached properties to efficiently manage file paths and
    provides methods for common development operations like building,
    uploading, and installing packages.

    :param package_name: The Python package name (with underscores)

    Properties:

    - ``package_name_slug``: Package name in slug format (with hyphens)
    - ``dir_repo``: Root directory for the project repository
    - ``dir_package``: Directory containing the Python package
    - ``path_*``: Various file paths within the project structure
    - ``dist_files``: List of built distribution files

    Example:
        >>> project = PyProjectStructure(package_name="my_awesome_package")
        >>> project.poetry_build()  # Build distributions
        >>> project.twine_upload()  # Upload to PyPI
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
        """
        Remove the entire project repository directory.

        This method safely removes the project's build directory and all its contents.
        It's typically used for cleaning up before a fresh build.
        """
        shutil.rmtree(self.dir_repo, ignore_errors=True)  # Safely remove directory tree

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
    def dir_dist(self) -> Path:
        """
        Get the distribution directory path for built packages.

        Example: ``build/repos/boto3_dataclass_ec2-project/dist``
        """
        return self.dir_repo / "dist"

    @cached_property
    def dist_files(self) -> list[str]:
        """
        Get the list of distribution files in the dist directory.

        Scans the project's dist/ directory for built distribution files
        (both wheel and source distributions) that belong to this package.

        Returns:
            List of absolute paths to distribution files as strings

        Example::

            [
                "build/repos/boto3_dataclass_ec2-project/dist/boto3_dataclass_ec2-0.1.1.tar.gz",
                "build/repos/boto3_dataclass_ec2-project/dist/boto3_dataclass_ec2-0.1.1-py3-none-any.whl"
            ]
        """
        dists = list()
        # Iterate through all files in the dist directory
        for p in self.dir_dist.iterdir():
            # Only include files that match our package name and are valid distribution types
            if p.name.startswith(self.package_name) and p.suffix in {".whl", ".tar.gz"}:
                dists.append(str(p))  # Convert Path to string for Twine compatibility

        return dists

    def poetry_build(self):
        """
        Build the package using Poetry.

        Creates both source distribution (.tar.gz) and wheel (.whl) files
        in the project's dist/ directory using Poetry's build command.

        Raises:
            subprocess.CalledProcessError: If the Poetry build command fails
        """
        args = ["poetry", "build"]
        # Change to project directory for build operation
        with temp_cwd(self.dir_repo):
            subprocess.run(args, cwd=self.dir_repo, check=True)  # Execute poetry build with error checking

    def twine_upload(self):
        """
        Upload distribution files to PyPI using Twine.

        Uploads all distribution files (both source and wheel) found in the
        dist/ directory to the configured PyPI repository using Twine.

        :raises:
            twine.exceptions.TwineException: If upload fails
            requests.exceptions.RequestException: If network error occurs
        """
        # Change to project directory for upload operation
        with temp_cwd(self.dir_repo):
            try:
                twine.commands.upload.upload(
                    upload_settings=config.twine_upload_settings,  # Use configured credentials/settings
                    dists=self.dist_files,  # Upload all built distribution files
                )
            except requests.exceptions.HTTPError as e:
                print(f"response.headers:")
                for k, v in e.response.headers.items():
                    print(f"{k} = {v}")
                print(f"response.text:")
                print(e.response.text)
                raise
            except Exception as e:
                print(f"{type(e) = }")
                raise

    def pip_install_editable(self):
        """
        Install the package in editable mode for development.

        Installs the package in development mode (editable install) using pip.
        This allows changes to the source code to be immediately reflected
        without reinstalling the package.

        Raises:
            subprocess.CalledProcessError: If the pip install command fails
        """
        # Use pip from project's virtual environment
        path_bin_pip = path_enum.dir_venv_bin / "pip"
        args = [
            f"{path_bin_pip}",
            "install",
            "-e",  # Editable/development mode flag
            ".",  # Install current directory
        ]
        # Change to project directory for installation
        with temp_cwd(self.dir_repo):
            subprocess.run(args, cwd=self.dir_repo, check=True)  # Execute pip install with error checking
