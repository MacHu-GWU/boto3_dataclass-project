# -*- coding: utf-8 -*-

"""
Boto3 Dataclass Service Structure Management.

It bridges the gap between installed mypy-boto3 stub packages and the generated
boto3-dataclass service packages.

The module handles:

- **Service Discovery**: Automatically discovers installed mypy-boto3 stub packages
- **Path Mapping**: Maps between source stub files and target dataclass package files
- **Service Name Translation**: Converts between AWS service names and package naming conventions
- **Stub File Location**: Provides paths to various mypy-boto3 stub files (client.pyi, type_defs.pyi, literals.pyi)
- **Build Target Paths**: Defines where generated dataclass files should be placed
- **Service Enumeration**: Lists all available AWS services with complete stub files

Key Concepts:

- **Service Name**: The AWS service identifier (e.g., "ec2", "s3")
- **Package Name**: The Python package name (e.g., "boto3_dataclass_ec2")
- **Stub Package**: The mypy-boto3 source package (e.g., "mypy_boto3_ec2")
- **Structure**: The complete project layout for a service-specific dataclass package
"""

import site
import dataclasses
from functools import cached_property
from pathlib import Path

from ..constants import PACKAGE_NAME_PREFIX
from .pyproject import PyProjectStructure

dir_site_packages = Path(site.getsitepackages()[0])


@dataclasses.dataclass
class Boto3DataclassServiceStructure(PyProjectStructure):
    """
    Structure manager for boto3 dataclass service packages.

    This class extends :class:`~boto3_dataclass.structures.pyproject.PyProjectStructure`
    to provide AWS service-specific functionality for managing the relationship
    between mypy-boto3 stub packages and generated boto3-dataclass packages.

    The class handles the complete lifecycle of service package structure:

    - Discovering installed mypy-boto3 stub packages in site-packages
    - Mapping service names to package naming conventions
    - Providing paths to both source stub files and target dataclass files
    - Managing the project structure for individual AWS services

    **Naming Conventions**:

    - Service name: "ec2" (AWS service identifier)
    - Package name: "boto3_dataclass_ec2" (generated package)
    - Stub package: "mypy_boto3_ec2" (source stub package)
    - Package slug: "boto3-dataclass-ec2" (PyPI/distribution name)

    **Path Structure**:

    The class manages paths for both source (mypy-boto3) and target (dataclass) files::

        site-packages/mypy_boto3_ec2/          # Source stub package
        ├── client.pyi                         # Client interface stubs
        ├── type_defs.pyi                      # Type definitions
        └── literals.pyi                       # Literal type definitions

        build/repos/boto3_dataclass_ec2-project/  # Target package structure
        ├── boto3_dataclass_ec2/
        │   ├── __init__.py
        │   ├── type_defs.py                   # Generated from type_defs.pyi
        │   └── caster.py                      # Generated from client.pyi
        ├── pyproject.toml
        ├── README.rst
        └── LICENSE.txt

    :param package_name: Inherited from PyProjectStructure, format: "boto3_dataclass_{service}"

    Example:
        >>> # Create structure for a specific service
        >>> structure = Boto3DataclassServiceStructure.new("s3")
        >>> structure.service_name  # "s3"
        >>> structure.package_name  # "boto3_dataclass_s3"
        >>>
        >>> # Get paths to stub files
        >>> structure.path_mypy_boto3_type_defs_pyi  # Path to mypy_boto3_s3/type_defs.pyi
        >>> structure.path_mypy_boto3_client_pyi     # Path to mypy_boto3_s3/client.pyi
        >>>
        >>> # Get paths for generated files
        >>> structure.path_boto3_dataclass_type_defs_py  # Where to write type_defs.py
        >>> structure.path_boto3_dataclass_caster_py     # Where to write caster.py
    """

    @classmethod
    def new(cls, service_name: str):
        """
        Create a new service structure for the specified AWS service.

        :param service_name: The AWS service name (e.g., "ec2", "s3", "lambda")

        :returns: A new :class:`Boto3DataclassServiceStructure` instance configured
            for the service

        Example:
            >>> structure = Boto3DataclassServiceStructure.new("ec2")
            >>> structure.service_name  # "ec2"
            >>> structure.package_name  # "boto3_dataclass_ec2"
        """
        return cls(package_name=f"{PACKAGE_NAME_PREFIX}_{service_name}")

    @cached_property
    def service_name(self) -> str:
        """
        Extract the AWS service name from the package name.

        :returns: The AWS service name (e.g., "ec2" from "boto3_dataclass_ec2")
        """
        return self.package_name.removeprefix(f"{PACKAGE_NAME_PREFIX}_")

    @cached_property
    def boto3_stubs_package_name(self) -> str:
        """
        Get the corresponding mypy-boto3 stub package name.

        :returns: The mypy-boto3 package name (e.g., "mypy_boto3_ec2")
        """
        return f"mypy_boto3_{self.service_name}"

    @cached_property
    def boto3_stubs_package_name_slug(self) -> str:
        """
        Get the mypy-boto3 package name in slug format (with hyphens).

        :returns: The slug format package name (e.g., "mypy-boto3-ec2")
        """
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
        Discover all available AWS services with complete mypy-boto3 stub packages.

        Scans the ``site-packages`` directory for ``mypy_boto3_*`` packages that contain
        both client.pyi and type_defs.pyi stub files, indicating they are complete
        and suitable for dataclass generation.

        :returns: List of :class:`Boto3DataclassServiceStructure` instances for each discovered service

        Example:
            >>> structures = Boto3DataclassServiceStructure.list_all()
            >>> service_names = [struct.service_name for struct in structures]
            >>> print(service_names)  # ["ec2", "s3", "lambda", "rds", ...]
        """
        service_list = list()

        # Scan site-packages for mypy-boto3 stub packages
        for path in dir_site_packages.iterdir():
            if path.name.startswith("mypy_boto3_"):
                # Only include packages with required stub files
                if (
                    path.joinpath("client.pyi").exists()
                    and path.joinpath("type_defs.pyi").exists()
                ):
                    # Extract service name and create structure
                    service_name = path.name.removeprefix("mypy_boto3_")
                    service_list.append(cls.new(service_name=service_name))

        return service_list

    @cached_property
    def path_boto3_dataclass_type_defs_py(self) -> Path:
        """
        Get the path where the generated type_defs.py file will be written.

        This file contains the dataclass definitions generated from the
        mypy-boto3 type_defs.pyi stub file.

        :returns: Path to the target type_defs.py file

        Example:
            ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/type_defs.py``
        """
        return self.dir_package / "type_defs.py"

    @cached_property
    def path_boto3_dataclass_caster_py(self) -> Path:
        """
        Get the path where the generated caster.py file will be written.

        This file contains utility functions for converting boto3 service responses
        into dataclass instances, generated from the mypy-boto3 client.pyi stub file.

        :returns: Path to the target caster.py file

        Example:
            ``build/repos/boto3_dataclass_ec2-project/boto3_dataclass_ec2/caster.py``
        """
        return self.dir_package / "caster.py"
