# -*- coding: utf-8 -*-

"""
This module provides utilities for access Jinja2 templates used in code generation.
It defines the :class:`TemplateEnum` class, which exposes cached properties for accessing templates.
"""

from functools import cached_property

from .template_helpers import load_template


class TemplateEnum:
    @cached_property
    def template_enum_py(self):
        return load_template("template_enum.py.jinja")
    
    @cached_property
    def type_defs__module(self):
        return load_template("type_defs/module.jinja")
    
    @cached_property
    def type_defs__typed_dict_def(self):
        return load_template("type_defs/typed_dict_def.jinja")
    
    @cached_property
    def type_defs__typed_dict_field(self):
        return load_template("type_defs/typed_dict_field.jinja")
    

tpl_enum = TemplateEnum()