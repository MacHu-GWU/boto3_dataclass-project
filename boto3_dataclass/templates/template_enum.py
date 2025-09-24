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
    def boto3_dataclass_service__typed_dict_def(self):
        return load_template("boto3_dataclass_service/typed_dict_def.jinja")
    
    @cached_property
    def boto3_dataclass_service__typed_dict_field(self):
        return load_template("boto3_dataclass_service/typed_dict_field.jinja")
    
    @cached_property
    def boto3_dataclass_service__type_defs_py(self):
        return load_template("boto3_dataclass_service/type_defs.py.jinja")
    

tpl_enum = TemplateEnum()