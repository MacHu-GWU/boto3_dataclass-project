# -*- coding: utf-8 -*-

"""
Project Structure Management for boto3-dataclass.

This module provides comprehensive project structure management classes that define
and manage the file system layout for different types of Python projects in the
boto3-dataclass ecosystem. The structures ensure proper path resolution, build
operations, and distribution management across various project types.

The module contains two main structure classes:

- :class:`~boto3_dataclass.structures.pyproject.PyProjectStructure`:
    Base structure for standard Python projects using Poetry
- :class:`~boto3_dataclass.structures.boto3_dataclass_service.Boto3DataclassServiceStructure`:
    Extended structure for AWS service-specific packages

All project types are Python projects at their core, making ``PyProjectStructure`` the
foundational class that handles common Python project operations like building with
Poetry, uploading to PyPI with Twine, and managing development installations.

The service-specific structure extends this base functionality to handle the unique
requirements of AWS service dataclass generation, including stub file discovery
and path mapping between mypy-boto3 sources and generated dataclass targets.
"""
