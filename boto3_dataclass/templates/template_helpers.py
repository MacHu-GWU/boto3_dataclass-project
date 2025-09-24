# -*- coding: utf-8 -*-

"""
Utilities for loading and managing Jinja2 templates used in code generation.

It generates the templates/template_enum.py file which contains an enumeration of all templates.
"""

import dataclasses
from pathlib import Path

import jinja2

from ..paths import path_enum


def load_template(relpath: str) -> jinja2.Template:
    """
    Load a Jinja2 template by relative path from the ``templates`` directory.

    :param relpath: The relative path of the template to load, using '/' as the separator.
        Example: ``type_defs/module.jinja``
    """
    parts = relpath.split("/")
    path = path_enum.dir_templates.joinpath(*parts)
    return jinja2.Template(path.read_text(encoding="utf-8"))


@dataclasses.dataclass
class TemplateMetadata:
    """
    Data container for metadata about a Jinja2 template file.
    """

    path: Path = dataclasses.field(default_factory=Path)

    @property
    def relpath(self) -> str:
        """
        The path of the template file relative to the ``templates`` directory.
        """
        return str(self.path.relative_to(path_enum.dir_templates))

    @property
    def name(self) -> str:
        """
        A valid Python identifier derived from the template's relative path.
        """
        return self.relpath.removesuffix(".jinja").replace("/", "__").replace(".", "_")


def gen_code():
    """
    Generate the templates/template_enum.py file containing an enumeration of all templates.
    """
    template = load_template("template_enum.py.jinja")
    template_metadata_list = list()
    for path in path_enum.dir_templates.rglob("*.jinja"):
        template_metadata = TemplateMetadata(path=path)
        template_metadata_list.append(template_metadata)
    code = template.render(template_metadata_list=template_metadata_list)
    path_out = path_enum.dir_templates / "template_enum.py"
    path_out.write_text(code, encoding="utf-8")
