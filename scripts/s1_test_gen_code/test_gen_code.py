# -*- coding: utf-8 -*-

from pathlib import Path
from boto3_dataclass.gen_code.gen_code import (
    TypedDictField,
    TypedDictDef,
    TypedDictDefMapping,
)

dir_here = Path(__file__).absolute().parent
path_code = dir_here / f"generated_code.py"

mapping = {
    "ProfileTypeDef": TypedDictDef(
        name="ProfileTypeDef",
        fields={
            "firstname": TypedDictField(
                name="firstname",
            ),
            "lastname": TypedDictField(
                name="lastname",
            ),
            "phone_number": TypedDictField(
                name="phone_number",
            ),
            "status": TypedDictField(
                name="status",
            ),
        },
    ),
    "UserTypeDef": TypedDictDef(
        name="UserTypeDef",
        fields={
            "user_id": TypedDictField(
                name="user_id",
            ),
            "profile": TypedDictField(
                name="profile",
                is_nested_typed_dict=True,
                nested_type_name="ProfileTypeDef",
            ),
            "labels": TypedDictField(
                name="labels",
            ),
            "tags": TypedDictField(
                name="tags",
            ),
        },
    ),
}
typed_dict_def_mapping = TypedDictDefMapping(mapping=mapping)
s = typed_dict_def_mapping.gen_code()
path_code.write_text(s, encoding="utf-8")
