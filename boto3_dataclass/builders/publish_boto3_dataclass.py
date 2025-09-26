# -*- coding: utf-8 -*-

"""
Main Boto3 Dataclass Package Builder.

This module provides the builder for the main ``boto3_dataclass`` package,
which serves as the umbrella package that imports and exposes all AWS service
dataclass packages. This package acts as the central entry point for users
who want access to all boto3 dataclass functionality.
"""

import dataclasses

from .._version import __version__
from ..templates.api import tpl_enum
from ..structures.api import PyProjectStructure, Boto3DataclassServiceStructure

from .publish_pyproject import PyProjectBuilder


@dataclasses.dataclass
class Boto3DataclassBuilder(PyProjectBuilder):
    """
    Builder for the main boto3_dataclass umbrella package.

    This class creates the main ``boto3_dataclass`` package that serves as an
    umbrella package importing and exposing all AWS service dataclass packages.
    It extends :class:`PyProjectBuilder` to provide specialized functionality
    for building the central package that users install to get access to all
    boto3 dataclass functionality.

    The builder handles:

    - Discovering all available AWS service packages
    - Generating imports for all service packages in __init__.py
    - Creating package dependencies on all service packages
    - Building package configuration files

    :param structure: PyProjectStructure instance for package management
    :param service_names: List of AWS service names to include in the package

    Example:
        >>> builder = Boto3DataclassBuilder.new(version="1.0.0")
        >>> builder.service_names  # ["ec2", "s3", "lambda", ...]
        >>> builder.build_all()  # Build complete package structure
        >>> builder.structure.poetry_build()  # Build with Poetry
        >>> builder.structure.twine_upload()  # Upload to PyPI

    Package Structure::

        build/repos/boto3_dataclass-project/
        ├── boto3_dataclass/
        │   └── __init__.py          # Imports all service packages
        ├── pyproject.toml           # Dependencies on all service packages
        ├── README.rst
        └── LICENSE.txt
    """

    structure: "PyProjectStructure" = dataclasses.field()
    service_names: list[str] = dataclasses.field(default_factory=list)

    @classmethod
    def new(
        cls,
        version: str = __version__,
        package_name: str = "boto3_dataclass",
    ):
        """
        Create a new Boto3DataclassBuilder with auto-discovered services.

        This factory method automatically discovers all available AWS services
        by scanning installed mypy-boto3 stub packages and creates a builder
        configured to include all of them.

        :param version: Package version for the main package
        :param package_name: Name of the main package (defaults to "boto3_dataclass")

        :returns: Configured :class:`Boto3DataclassBuilder` instance

        Example:
            >>> builder = Boto3DataclassBuilder.new(version="1.2.0")
            >>> len(builder.service_names)  # Number of discovered services
            50+
        """
        structure_list = Boto3DataclassServiceStructure.list_all()
        service_names = [struct.service_name for struct in structure_list]
        return cls(
            version=version,
            structure=PyProjectStructure(package_name=package_name),
            service_names=service_names,
        )

    def log(self, ith: int | None = None):
        """
        Log the current package being worked on with its repository path.

        :param ith: Optional sequence number (unused in main package building)
        """
        path = f"file://{self.structure.dir_repo}"
        print(f"========== Work on {self.structure.package_name}: {path}")

    def build_all(self):
        """
        Build all components of the main boto3_dataclass package.

        This method orchestrates the complete build process for the umbrella package:

        1. Cleans the output directory
        2. Creates boto3_dataclass/__init__.py with imports for all services
        3. Creates pyproject.toml with dependencies on all service packages
        4. Creates README.rst documentation
        5. Creates LICENSE.txt file

        The resulting package structure allows users to ``import boto3_dataclass``
        and access all AWS service dataclasses through a single import.
        """
        self.structure.remove_dir()
        self.build_init_py()
        self.build_pyproject_toml()
        self.build_README_rst()
        self.build_LICENSE_txt()

    def build_init_py(self):
        """
        Build the main package ``__init__.py`` file from template.

        Creates the package initialization file that imports and exposes
        all available AWS service dataclass packages. This allows users
        to access all functionality through the main package.
        """
        path = self.structure.path_init_py
        tpl = tpl_enum.boto3_dataclass__package____init___py
        self.build_by_template(path, tpl)

    def build_pyproject_toml(self):
        """
        Build the ``pyproject.toml`` configuration file from template.

        Creates the Poetry/PEP 518 project configuration file with:

        - Package metadata and description
        - Dependencies on all service-specific dataclass packages
        - Optional dependencies
        - Build system configuration
        """
        path = self.structure.path_pyproject_toml
        tpl = tpl_enum.boto3_dataclass__pyproject_toml
        self.build_by_template(path, tpl)

    def build_README_rst(self):
        """
        Build the ``README.rst`` documentation file from template.

        Creates the package documentation with:

        - Installation instructions
        - Usage examples showing how to use different services
        - API reference and available services list
        """
        path = self.structure.path_README_rst
        tpl = tpl_enum.boto3_dataclass__README_rst
        self.build_by_template(path, tpl)

    def build_LICENSE_txt(self):
        """
        Build the ``LICENSE.txt`` file from template.

        Creates the software license file for the package distribution.
        Uses the common license template shared across all packages.
        """
        path = self.structure.path_LICENSE_txt
        tpl = tpl_enum.common__LICENSE_txt
        self.build_by_template(path, tpl)
