# -*- coding: utf-8 -*-

"""
Boto3 Dataclass Service Package Builder.

This module provides functionality for building and publishing boto3 dataclass service packages.
It generates Python packages that provide dataclass wrappers for AWS services, making it easier
to work with boto3 responses in a type-safe manner.

The main components include:

- Parse type definitions from mypy-boto3 stubs
- Creating caster utilities for converting boto3 responses to dataclasses
- Generating package configuration files (pyproject.toml, README, LICENSE)
- Parallel processing for bulk package building and uploading
"""

import typing as T
import time
import dataclasses

import mpire
from tenacity import retry, stop_after_attempt, wait_fixed, wait_chain

from .._version import __version__
from ..utils import black_format_code, write
from ..templates.api import tpl_enum
from ..structures.api import Boto3DataclassServiceStructure
from ..parsers.api import TypedDefsModuleParser
from ..parsers.api import ClientModuleParser

from .publish_pyproject import PyProjectBuilder

if T.TYPE_CHECKING:  # pragma: no cover
    from ..pypi import T_PACKAGE_STATUS_INFO


@dataclasses.dataclass
class Boto3DataclassServiceBuilder(PyProjectBuilder):
    """
    Builder for boto3 dataclass service packages.

    This class handles the complete build process for boto3 dataclass service packages,
    including parsing mypy-boto3 stubs, generating dataclass wrappers, creating package
    configuration files, and managing parallel builds/uploads.

    The builder transforms mypy-boto3 type stubs into usable dataclass packages that
    provide type-safe wrappers around boto3 service responses.

    :param version: Package version (inherited from PyProjectBuilder)
    :param structure: The service structure containing paths and metadata for the package

    Example:
        >>> structure = Boto3DataclassServiceStructure.new("s3")
        >>> builder = Boto3DataclassServiceBuilder(version="1.0.0", structure=structure)
        >>> builder.build_all() # Build all package components at build/repos/boto3_dataclass_s3-project
        >>> builder.structure.poetry_build()  # Build the package
        >>> builder.structure.twine_upload()  # Upload to PyPI

    Example package structure::

        build
        |-- repos
            |-- boto3_dataclass_{service_name}-project
                |-- boto3_dataclass_{service_name}
                    |-- __init__.py
                    |-- caster.py
                    |-- type_defs.py
                |-- LICENSE.txt
                |-- README.rst
                |-- pyproject.toml
    """

    structure: "Boto3DataclassServiceStructure" = dataclasses.field()

    def log(self, ith: int | None = None):
        """
        Log the current service being worked on with its repository path.

        Args:
            ith: Optional sequence number for parallel processing identification
        """
        path = f"file://{self.structure.dir_repo}"
        if ith:
            seq = f"{ith} "  # Add sequence number for parallel processing tracking
        else:
            seq = ""
        print(f"========== Work on {seq}{self.structure.service_name}: {path}")

    def build_all(self):
        """
        Build all components of the boto3 dataclass service package.

        This method orchestrates the complete build process:

        1. Cleans the output directory
        2. Creates boto3_dataclass_{service}/type_defs.py,
            type definitions from mypy-boto3 stubs
        3. Creates boto3_dataclass_{service}/caster.py,
            caster utilities for type conversion
        4. Creates boto3_dataclass_{service}/__init__.py,
        6. Creates pyproject.toml
        7. Creates README.rst
        8. Creates LICENSE.txt
        """
        self.structure.remove_dir()  # Clean existing build artifacts
        self.build_type_defs_py()
        self.build_caster_py()
        self.build_init_py()
        self.build_pyproject_toml()
        self.build_README_rst()
        self.build_LICENSE_txt()

    def build_type_defs_py(self):
        """
        Build type definitions module by parsing mypy-boto3 type stubs.

        This method:

        1. Parses the mypy-boto3 type_defs.pyi stub file
        2. Generates corresponding dataclass definitions
        3. Formats the code with black
        4. Writes the final ``type_defs.py`` file
        """
        # Parse mypy_boto3_{service_name}/type_defs.pyi stub file
        path_stub_file = self.structure.path_mypy_boto3_type_defs_pyi
        tdm_parser = TypedDefsModuleParser(path_stub_file=path_stub_file)
        tdm = tdm_parser.parse()

        # Generate boto3_dataclass_{service_name}/type_defs.py with import reference
        mypy_package_name = f"mypy_boto3_{self.structure.service_name}"
        type_defs_line = f"from {mypy_package_name} import type_defs"
        path = self.structure.path_boto3_dataclass_type_defs_py
        code = tdm.gen_code(type_defs_line=type_defs_line)

        # Format code with black formatter for consistency
        code = black_format_code(code)
        # Write the generated code to the target file
        write(path, code)

    def build_caster_py(self):
        """
        Build caster utilities for converting boto3 responses to dataclasses.

        This method:

        1. Parses the mypy-boto3 client.pyi stub file
        2. Generates caster functions for each service operation
        3. Formats and writes the ``caster.py`` module
        """
        # Parse mypy-boto3 client stub file for operation signatures
        path_stub_file = self.structure.path_mypy_boto3_client_pyi
        cm_parser = ClientModuleParser(path_stub_file=path_stub_file)
        cm = cm_parser.parse()

        # Generate caster utilities code
        path = self.structure.path_boto3_dataclass_caster_py
        code = cm.gen_code()

        # Format code with black formatter for consistency
        code = black_format_code(code)
        # Write the generated caster code
        write(path, code)

    def build_init_py(self):
        """
        Build the package ``__init__.py`` file from template.

        Creates the main package initialization file that exports
        the public API for the dataclass service package.
        """
        path = self.structure.path_init_py
        tpl = tpl_enum.boto3_dataclass_service__package____init___py
        self.build_by_template(path, tpl)

    def build_pyproject_toml(self):
        """
        Build the ``pyproject.toml`` configuration file from template.

        Creates the Poetry/PEP 518 project configuration file with
        package metadata, dependencies, and build system configuration.
        """
        path = self.structure.path_pyproject_toml
        tpl = tpl_enum.boto3_dataclass_service__pyproject_toml
        self.build_by_template(path, tpl)

    def build_README_rst(self):
        """
        Build the ``README.rst`` documentation file from template.

        Creates the package documentation with usage examples,
        installation instructions, and API reference.
        """
        path = self.structure.path_README_rst
        tpl = tpl_enum.boto3_dataclass_service__README_rst
        self.build_by_template(path, tpl)

    def build_LICENSE_txt(self):
        """
        Build the ``LICENSE.txt`` file from template.

        Creates the software license file for the package distribution.
        """
        path = self.structure.path_LICENSE_txt
        tpl = tpl_enum.common__LICENSE_txt
        self.build_by_template(path, tpl)

    @classmethod
    def list_all(
        cls,
        version: str = __version__,
    ) -> list["Boto3DataclassServiceBuilder"]:
        """
        Create builder instances for all available AWS services.

        :param version: Package version to assign to all builders

        :returns: List of :class:`Boto3DataclassServiceBuilder` instances,
            one for each AWS service
        """
        structure_list = Boto3DataclassServiceStructure.list_all()
        return [
            cls(version=version, structure=structure) for structure in structure_list
        ]

    @classmethod
    def list_filtered_sorted_all(
        cls,
        version: str = __version__,
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ) -> list["Boto3DataclassServiceBuilder"]:
        """
        List, filter, and sort all available service packages.

        :param version: Package version for builders
        :param package_status_info: Dict of package statuses to filter completed packages
        :param limit: Maximum number of packages to process
        """
        if package_status_info is None:
            package_status_info = {}

        # Get all available service packages
        package_list = cls.list_all(version=version)

        # Filter out packages that are already completed/published
        filtered_package_list = [
            package
            for package in package_list
            if package_status_info.get(package.structure.package_name_slug, False)
            is False
        ]

        # Sort packages alphabetically for consistent processing order
        sorted_package_list = list(
            sorted(
                filtered_package_list,
                key=lambda p: p.structure.package_name_slug,
            ),
        )

        # Apply limit if specified
        if limit is not None:
            sorted_package_list = sorted_package_list[:limit]

        return sorted_package_list

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
        """
        Execute a function in parallel across multiple service packages.

        This is a private method that handles the parallel execution infrastructure
        for batch operations on service packages.

        :param func: Function to execute for each package (takes index and builder)
        :param version: Package version for builders
        :param n_workers: Number of worker processes (None for auto-detection)
        :param start_method: Multiprocessing start method ("fork" or "threading")
        :param package_status_info: Dict of package statuses to filter completed packages
        :param limit: Maximum number of packages to process
        """
        sorted_package_list = cls.list_filtered_sorted_all(
            version=version,
            package_status_info=package_status_info,
            limit=limit,
        )
        # Create task list with sequence numbers for logging
        tasks = [
            {"ith": i, "package": package}
            for i, package in enumerate(sorted_package_list, start=1)
        ]

        # Execute tasks in parallel using mpire worker pool
        with mpire.WorkerPool(n_jobs=n_workers, start_method=start_method) as pool:
            results = pool.map(
                func,
                tasks,
            )  # Results not used but kept for potential future use

    @classmethod
    def parallel_build_all(
        cls,
        version: str = __version__,
        n_workers: int | None = None,
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ):
        """
        Build all boto3 dataclass service packages in parallel.

        This method orchestrates parallel building of multiple AWS service packages,
        using multiprocessing to speed up the build process.

        :param version: Package version for all built packages
        :param n_workers: Number of worker processes (None for auto-detection)
        :param package_status_info: Dict tracking package completion status
        :param limit: Maximum number of packages to build
        """

        def main(ith: int, package: "Boto3DataclassServiceBuilder"):
            """Worker function that builds a single service package."""
            package.log(ith)  # Log which package is being processed
            package.build_all()  # Execute full build process

        cls._parallel_run(
            version=version,
            func=main,
            n_workers=n_workers,
            start_method="fork",  # Use fork for CPU-intensive build operations
            package_status_info=package_status_info,
            limit=limit,
        )

    @classmethod
    def parallel_poetry_build_all(
        cls,
        version: str = __version__,
        n_workers: int | None = None,
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ):
        """
        Build all boto3 dataclass service packages with Poetry in parallel.

        :param version: Package version for all built packages
        :param n_workers: Number of worker threads (None for auto-detection)
        :param package_status_info: Dict tracking package upload status
        :param limit: Maximum number of packages to upload
        """
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
        def main(ith: int, package: "Boto3DataclassServiceBuilder"):
            """Worker function that builds a single service package."""
            package.log(ith)  # Log which package is being processed
            package.structure.poetry_build()  # Build the package with Poetry
            if len(package.structure.dist_files) == 2:
                raise ValueError(
                    f"{package.structure.dir_dist} doesn't have exactly 2 files",
                )

        cls._parallel_run(
            version=version,
            func=main,
            n_workers=n_workers,
            start_method="fork",  # Use fork for CPU-intensive build operations
            package_status_info=package_status_info,
            limit=limit,
        )

    @classmethod
    def sequence_upload_all(
        cls,
        version: str = __version__,
        package_status_info: T.Optional["T_PACKAGE_STATUS_INFO"] = None,
        limit: int | None = None,
    ):
        """
        Build and upload all boto3 dataclass service packages to PyPI in sequence.
        We don't do parallel upload to avoid hitting PyPI rate limits.

        :param version: Package version for all built packages
        :param n_workers: Number of worker threads (None for auto-detection)
        :param package_status_info: Dict tracking package upload status
        :param limit: Maximum number of packages to upload
        """

        @retry(
            stop=stop_after_attempt(5),
            wait=wait_chain(
                wait_fixed(600),
                wait_fixed(1200),
                wait_fixed(1800),
                wait_fixed(3600),
            )
        )
        def main(ith: int, package: "Boto3DataclassServiceBuilder"):
            """Worker function that builds and uploads a single service package."""
            package.log(ith)  # Log which package is being processed
            package.structure.twine_upload()  # Upload to PyPI with twine

        sorted_package_list = cls.list_filtered_sorted_all(
            version=version,
            package_status_info=package_status_info,
            limit=limit,
        )
        tasks = [
            {"ith": i, "package": package}
            for i, package in enumerate(sorted_package_list, start=1)
        ]
        for task in tasks:
            main(**task)
            time.sleep(10)  # Sleep to avoid hitting PyPI rate limits
