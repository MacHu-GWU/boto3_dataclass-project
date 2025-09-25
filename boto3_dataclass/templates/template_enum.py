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
    def boto3_dataclass_service__README_rst(self):
        return load_template("boto3_dataclass_service/README.rst.jinja")
    
    @cached_property
    def boto3_dataclass_service__pyproject_toml(self):
        return load_template("boto3_dataclass_service/pyproject.toml.jinja")
    
    @cached_property
    def boto3_dataclass_service__package__caster_py(self):
        return load_template("boto3_dataclass_service/package/caster.py.jinja")
    
    @cached_property
    def boto3_dataclass_service__package__typed_dict_def(self):
        return load_template("boto3_dataclass_service/package/typed_dict_def.jinja")
    
    @cached_property
    def boto3_dataclass_service__package__caster_method(self):
        return load_template("boto3_dataclass_service/package/caster_method.jinja")
    
    @cached_property
    def boto3_dataclass_service__package__typed_dict_field(self):
        return load_template("boto3_dataclass_service/package/typed_dict_field.jinja")
    
    @cached_property
    def boto3_dataclass_service__package____init___py(self):
        return load_template("boto3_dataclass_service/package/__init__.py.jinja")
    
    @cached_property
    def boto3_dataclass_service__package__type_defs_py(self):
        return load_template("boto3_dataclass_service/package/type_defs.py.jinja")
    
    @cached_property
    def common__LICENSE_txt(self):
        return load_template("common/LICENSE.txt.jinja")
    
    @cached_property
    def boto3_dataclass__README_rst(self):
        return load_template("boto3_dataclass/README.rst.jinja")
    
    @cached_property
    def boto3_dataclass__LICENSE_txt(self):
        return load_template("boto3_dataclass/LICENSE.txt.jinja")
    
    @cached_property
    def boto3_dataclass__pyproject_toml(self):
        return load_template("boto3_dataclass/pyproject.toml.jinja")
    
    @cached_property
    def boto3_dataclass__package____init___py(self):
        return load_template("boto3_dataclass/package/__init__.py.jinja")
    

tpl_enum = TemplateEnum()