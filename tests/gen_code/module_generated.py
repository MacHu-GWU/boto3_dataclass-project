# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, List, Dict
import dataclasses
from functools import cached_property

from boto3_dataclass.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from boto3_dataclass.tests.gen_code import type_defs


@dataclasses.dataclass(frozen=True)
class SimpleModel(Base["type_defs.SimpleModelTypeDef"]):
    @cached_property
    def attr1(self):
        return self._data["attr1"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithSubscript(Base["type_defs.SimpleModelWithSubscriptTypeDef"]):
    @cached_property
    def attr1(self):
        return self._data["attr1"]

    @cached_property
    def attr2(self):
        return self._data["attr2"]

    @cached_property
    def attr3(self):
        return self._data["attr3"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithNestedSubscript(Base["type_defs.SimpleModelWithNestedSubscriptTypeDef"]):
    @cached_property
    def attr1(self):
        return self._data["attr1"]

    @cached_property
    def attr2(self):
        return self._data["attr2"]


@dataclasses.dataclass(frozen=True)
class SimpleContainer(Base["type_defs.SimpleContainerTypeDef"]):
    @cached_property
    def attr1(self):
        return SimpleModel.make_one(self._data["attr1"])

    @cached_property
    def attr2(self):
        return SimpleModel.make_one(self._data["attr2"])

    @cached_property
    def attr3(self):
        return SimpleModel.make_one(self._data["attr3"])

    @cached_property
    def attr4(self):
        return SimpleModel.make_one(self._data["attr4"])

    @cached_property
    def attr5(self):
        return SimpleModel.make_one(self._data["attr5"])

    @cached_property
    def attr6(self):
        return SimpleModel.make_one(self._data["attr6"])

    @cached_property
    def attr7(self):
        return [SimpleModel.make_one(dct) for dct in self._data["attr7"]]

    @cached_property
    def attr8(self):
        return [SimpleModel.make_one(dct) for dct in self._data["attr8"]]

