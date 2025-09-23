# -*- coding: utf-8 -*-

"""
This module provides utilities for loading Jinja2 templates used in code generation.
It defines the :class:`TplEnum` class, which exposes cached properties for accessing templates
related to TypedDict fields, TypedDict definitions, and module structure.
Templates are loaded from the 'tpl' directory located alongside this module.
"""

from pathlib import Path
from functools import cached_property

import jinja2

dir_here = Path(__file__).absolute().parent
dir_tpl = dir_here / "tpl"


def load_template(name: str) -> jinja2.Template:
    """
    Load a Jinja2 template by name from the 'tpl' directory.

    :param name: The filename of the template to load.
    :return: A Jinja2 Template object.
    """
    path = dir_tpl / name
    return jinja2.Template(path.read_text(encoding="utf-8"))


class TplEnum:
    """
    Provides access to Jinja2 templates used for code generation.

    Cached properties are available for templates related to TypedDict fields,
    TypedDict definitions, and module structure.
    """

    @cached_property
    def typed_dict_field(self) -> jinja2.Template:
        """
        Get the Jinja2 template for a TypedDict field.

        :return: A Jinja2 Template object for TypedDict fields.
        """
        return load_template("typed_dict_field.jinja")

    @cached_property
    def typed_dict_def(self) -> jinja2.Template:
        """
        Get the Jinja2 template for a TypedDict definition.

        :return: A Jinja2 Template object for TypedDict definitions.
        """
        return load_template("typed_dict_def.jinja")

    @cached_property
    def module(self) -> jinja2.Template:
        """
        Get the Jinja2 template for a module structure.

        :return: A Jinja2 Template object for module structure.
        """
        return load_template("module.jinja")


tpl_enum = TplEnum()
