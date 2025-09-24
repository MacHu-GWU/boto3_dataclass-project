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

    @classmethod
    def make_one(cls, boto3_raw_data: T.Optional["type_defs.SimpleModelTypeDef"]):
        if boto3_raw_data is None:
            return None
        return cls(boto3_raw_data=boto3_raw_data)

    @classmethod
    def make_many(cls, boto3_raw_data_list: T.Optional[T.Iterable["type_defs.SimpleModelTypeDef"]]):
        if boto3_raw_data_list is None:
            return None
        return [cls(boto3_raw_data=boto3_raw_data) for boto3_raw_data in boto3_raw_data_list]

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

    @classmethod
    def make_one(cls, boto3_raw_data: T.Optional["type_defs.SimpleModelWithSubscriptTypeDef"]):
        if boto3_raw_data is None:
            return None
        return cls(boto3_raw_data=boto3_raw_data)

    @classmethod
    def make_many(cls, boto3_raw_data_list: T.Optional[T.Iterable["type_defs.SimpleModelWithSubscriptTypeDef"]]):
        if boto3_raw_data_list is None:
            return None
        return [cls(boto3_raw_data=boto3_raw_data) for boto3_raw_data in boto3_raw_data_list]

@dataclasses.dataclass(frozen=True)
class SimpleModelWithNestedSubscript:
    boto3_raw_data: "type_defs.SimpleModelWithNestedSubscriptTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):  # pragma: no cover
        return self.boto3_raw_data["attr1"]

    @cached_property
    def attr2(self):  # pragma: no cover
        return self.boto3_raw_data["attr2"]

    @classmethod
    def make_one(cls, boto3_raw_data: T.Optional["type_defs.SimpleModelWithNestedSubscriptTypeDef"]):
        if boto3_raw_data is None:
            return None
        return cls(boto3_raw_data=boto3_raw_data)

    @classmethod
    def make_many(cls, boto3_raw_data_list: T.Optional[T.Iterable["type_defs.SimpleModelWithNestedSubscriptTypeDef"]]):
        if boto3_raw_data_list is None:
            return None
        return [cls(boto3_raw_data=boto3_raw_data) for boto3_raw_data in boto3_raw_data_list]

@dataclasses.dataclass(frozen=True)
class SimpleContainer:
    boto3_raw_data: "type_defs.SimpleContainerTypeDef" = dataclasses.field()

    @cached_property
    def attr1(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr1"])

    @cached_property
    def attr2(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr2"])

    @cached_property
    def attr3(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr3"])

    @cached_property
    def attr4(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr4"])

    @cached_property
    def attr5(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr5"])

    @cached_property
    def attr6(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr6"])

    @cached_property
    def attr7(self):  # pragma: no cover
        return SimpleModel.make_many(self.boto3_raw_data["attr7"])

    @cached_property
    def attr8(self):  # pragma: no cover
        return SimpleModel.make_many(self.boto3_raw_data["attr8"])

    @cached_property
    def attr9(self):  # pragma: no cover
        return SimpleModel.make_many(self.boto3_raw_data["attr9"])

    @classmethod
    def make_one(cls, boto3_raw_data: T.Optional["type_defs.SimpleContainerTypeDef"]):
        if boto3_raw_data is None:
            return None
        return cls(boto3_raw_data=boto3_raw_data)

    @classmethod
    def make_many(cls, boto3_raw_data_list: T.Optional[T.Iterable["type_defs.SimpleContainerTypeDef"]]):
        if boto3_raw_data_list is None:
            return None
        return [cls(boto3_raw_data=boto3_raw_data) for boto3_raw_data in boto3_raw_data_list]

@dataclasses.dataclass(frozen=True)
class User:
    boto3_raw_data: "type_defs.UserTypeDef" = dataclasses.field()

    @cached_property
    def id(self):  # pragma: no cover
        return self.boto3_raw_data["id"]

    @cached_property
    def name(self):  # pragma: no cover
        return self.boto3_raw_data["name"]

    @cached_property
    def attr1(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr1"])

    @cached_property
    def attr2(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr2"])

    @cached_property
    def attr3(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr3"])

    @cached_property
    def attr4(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr4"])

    @cached_property
    def attr5(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr5"])

    @cached_property
    def attr6(self):  # pragma: no cover
        return SimpleModel.make_one(self.boto3_raw_data["attr6"])

    @cached_property
    def attr7(self):  # pragma: no cover
        return SimpleModel.make_many(self.boto3_raw_data["attr7"])

    @cached_property
    def attr8(self):  # pragma: no cover
        return SimpleModel.make_many(self.boto3_raw_data["attr8"])

    @cached_property
    def attr9(self):  # pragma: no cover
        return SimpleModel.make_many(self.boto3_raw_data["attr9"])

    @classmethod
    def make_one(cls, boto3_raw_data: T.Optional["type_defs.UserTypeDef"]):
        if boto3_raw_data is None:
            return None
        return cls(boto3_raw_data=boto3_raw_data)

    @classmethod
    def make_many(cls, boto3_raw_data_list: T.Optional[T.Iterable["type_defs.UserTypeDef"]]):
        if boto3_raw_data_list is None:
            return None
        return [cls(boto3_raw_data=boto3_raw_data) for boto3_raw_data in boto3_raw_data_list]
