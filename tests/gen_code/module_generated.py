# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from functools import cached_property

if T.TYPE_CHECKING:  # pragma: no cover
    from boto3_dataclass.tests.gen_code import type_defs


@dataclasses.dataclass(frozen=True)
class SimpleModel:
    boto3_raw_data: "type_defs.SimpleModelTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):  # pragma: no cover
        return self.boto3_raw_data["attr1"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithSubscript:
    boto3_raw_data: "type_defs.SimpleModelWithSubscriptTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):  # pragma: no cover
        return self.boto3_raw_data["attr1"]

    @cached_property
    def attr2(self):  # pragma: no cover
        return self.boto3_raw_data["attr2"]

    @cached_property
    def attr3(self):  # pragma: no cover
        return self.boto3_raw_data["attr3"]


@dataclasses.dataclass(frozen=True)
class SimpleModelWithNestedSubscript:
    boto3_raw_data: "type_defs.SimpleModelWithNestedSubscriptTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):  # pragma: no cover
        return self.boto3_raw_data["attr1"]

    @cached_property
    def attr2(self):  # pragma: no cover
        return self.boto3_raw_data["attr2"]


@dataclasses.dataclass(frozen=True)
class SimpleContainer:
    boto3_raw_data: "type_defs.SimpleContainerTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):  # pragma: no cover
        return SimpleModel(self.boto3_raw_data["attr1"])

    @cached_property
    def attr2(self):  # pragma: no cover
        return SimpleModel(self.boto3_raw_data["attr2"])

    @cached_property
    def attr3(self):  # pragma: no cover
        return SimpleModel(self.boto3_raw_data["attr3"])

    @cached_property
    def attr4(self):  # pragma: no cover
        return SimpleModel(self.boto3_raw_data["attr4"])

    @cached_property
    def attr5(self):  # pragma: no cover
        return SimpleModel(self.boto3_raw_data["attr5"])

    @cached_property
    def attr6(self):  # pragma: no cover
        return SimpleModel(self.boto3_raw_data["attr6"])

    @cached_property
    def attr7(self):  # pragma: no cover
        return [SimpleModel(dct) for dct in self.boto3_raw_data["attr7"]]

    @cached_property
    def attr8(self):  # pragma: no cover
        return [SimpleModel(dct) for dct in self.boto3_raw_data["attr8"]]

