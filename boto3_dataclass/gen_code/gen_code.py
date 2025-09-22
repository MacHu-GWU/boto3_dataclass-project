# -*- coding: utf-8 -*-

import dataclasses
from functools import cached_property

from .template import tpl_enum


@dataclasses.dataclass
class TypedDictField:
    name: str = dataclasses.field()
    is_nested_typed_dict: bool = dataclasses.field()
    type_name: str | None = dataclasses.field()


@dataclasses.dataclass
class TypedDictDef:
    name: str = dataclasses.field()
    fields: dict[str, TypedDictField] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class TypedDictDefMapping:
    mapping: dict[str, TypedDictDef] = dataclasses.field(default_factory=dict)
