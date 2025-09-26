# -*- coding: utf-8 -*-

"""
PyProject Template Builder.

This module provides the base builder class for Python project generation using
Jinja2 templates. It handles semantic versioning and template rendering for
creating Python project files like ``{package_name}/__init__.py``,
``pyproject.toml``, ``README.rst``  ``LICENSE.txt`` files, and other project components.
"""

import dataclasses
from pathlib import Path
from functools import cached_property

from jinja2 import Template

from ..utils import write, SemVer


@dataclasses.dataclass
class PyProjectBuilder:
    """
    Base builder class for Python project generation using Jinja2 templates.

    This class provides the core functionality for building Python projects from
    templates, with built-in semantic version parsing and template rendering
    capabilities. It serves as the foundation for more specialized builders
    in the boto3-dataclass ecosystem.

    The class handles:

    - Semantic version parsing and management
    - Jinja2 template rendering with builder context
    - File generation and writing utilities

    :param version: The semantic version string for the project (e.g., "1.2.3")

    Example:
        >>> builder = PyProjectBuilder(version="1.2.3")
        >>> builder.sem_ver.major  # 1
        >>> builder.sem_ver.minor  # 2
        >>> builder.sem_ver.patch  # 3
    """

    version: str = dataclasses.field()

    @cached_property
    def sem_ver(self) -> SemVer:
        """
        Parse and cache the semantic version information.

        :returns: A :class:`~boto3_dataclass.utils.SemVer` object containing
            parsed major, minor, and patch version components
        """
        return SemVer.parse(self.version)

    def build_by_template(
        self,
        path: Path,
        template: Template,
    ):
        """
        Render a Jinja2 template and write the output to a file.

        This method provides the core template rendering functionality used by
        all specialized builders. The template is rendered with the builder
        instance as context, allowing templates to access version information
        and other builder properties.

        :param path: Target file path where the rendered template will be written
        :param template: Jinja2 template instance to render

        Example:
            >>> from jinja2 import Template
            >>> template = Template("Version: {{ builder.version }}")
            >>> builder.build_by_template(Path("output.txt"), template)
            # Creates file with content: "Version: 1.2.3"
        """
        code = template.render(builder=self)
        write(path, code)
