# -*- coding: utf-8 -*-

from pathlib import Path
from boto3_dataclass.gen_code.gen_code import (
    TypedDictField,
    TypedDictDef,
    TypedDictDefMapping,
)

from ...paths import dir_unit_test

dir_here = Path(__file__).absolute().parent
path_generated_module = dir_unit_test / "gen_code" / f"module_generated.py"

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
