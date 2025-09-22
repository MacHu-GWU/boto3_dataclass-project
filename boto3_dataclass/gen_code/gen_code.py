# -*- coding: utf-8 -*-

import dataclasses
from functools import cached_property

from .template import tpl_enum


@dataclasses.dataclass
class TypedDictField:
    name: str = dataclasses.field()
    is_nested_typed_dict: bool = dataclasses.field(default=False)
    nested_type_name: str | None = dataclasses.field(default=None)

    @property
    def nested_modeL_name(self) -> str:
        return self.nested_type_name.removesuffix("TypeDef")

    def gen_code(self) -> str:
        return tpl_enum.typed_dict_field.render(tdf=self)


@dataclasses.dataclass
class TypedDictDef:
    name: str = dataclasses.field()
    fields: dict[str, TypedDictField] = dataclasses.field(default_factory=dict)

    @property
    def model_name(self) -> str:
        return self.name.removesuffix("TypeDef")

    def gen_code(self) -> str:
        return tpl_enum.typed_dict_def.render(td=self)


@dataclasses.dataclass
class TypedDictDefMapping:
    mapping: dict[str, TypedDictDef] = dataclasses.field(default_factory=dict)

    def gen_code(self) -> str:
        return tpl_enum.module.render(tddm=self)
