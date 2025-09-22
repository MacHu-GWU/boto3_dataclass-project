# -*- coding: utf-8 -*-

from boto3_dataclass.gen_code.gen_code import (
    TypedDictField,
    TypedDictDef,
    TypedDictDefMapping,
)

defs = [
    TypedDictDef(
        name="ProfileTypeDef",
        fields=[
            TypedDictField(name="firstname"),
            TypedDictField(name="lastname"),
            TypedDictField(name="phone_number"),
            TypedDictField(name="status"),
        ],
    ),
    TypedDictDef(
        name="UserTypeDef",
        fields=[
            TypedDictField(name="user_id"),
            TypedDictField(
                name="profile",
                is_nested_typed_dict=True,
                nested_type_name="ProfileTypeDef",
            ),
            TypedDictField(name="labels"),
            TypedDictField(name="tags"),
        ],
    ),
]

tddm = TypedDictDefMapping(defs=defs)
