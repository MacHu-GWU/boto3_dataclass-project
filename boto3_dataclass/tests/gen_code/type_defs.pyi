# -*- coding: utf-8 -*-

from typing import TypedDict, Required, NotRequired, Optional, Dict, List

from iterals import ProfileStatusType

class SimpleModelTypeDef(TypedDict):
    attr1: str

class SimpleModelWithSubscriptTypeDef(TypedDict):
    attr1: Required[str]
    attr2: NotRequired[str]
    attr3: List[str]

class SimpleModelWithNestedSubscriptTypeDef(TypedDict):
    attr1: Required[List[str]]
    attr2: NotRequired[List[str]]

class SimpleContainerTypeDef(TypedDict):
    attr1: SimpleModelTypeDef
    attr2: Optional[SimpleModelTypeDef]
    attr3: Required[SimpleModelTypeDef]
    attr4: NotRequired[SimpleModelTypeDef]
    attr5: Required[Optional[SimpleModelTypeDef]]
    attr6: NotRequired[Optional[SimpleModelTypeDef]]
    # 注: 我们没测 Optional[List[SimpleModelTypeDef]] 是因为它不合理
    attr7: List[SimpleModelTypeDef]
    attr8: Required[List[SimpleModelTypeDef]]
    attr9: NotRequired[List[SimpleModelTypeDef]]

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "id": int,
        "name": str,
        "attr1": SimpleModelTypeDef,
        "attr2": Optional[SimpleModelTypeDef],
        "attr3": Required[SimpleModelTypeDef],
        "attr4": NotRequired[SimpleModelTypeDef],
        "attr5": Required[Optional[SimpleModelTypeDef]],
        "attr6": NotRequired[Optional[SimpleModelTypeDef]],
        # 注: 我们没测 Optional[List[SimpleModelTypeDef]] 是因为它不合理
        "attr7": List[SimpleModelTypeDef],
        "attr8": Required[List[SimpleModelTypeDef]],
        "attr9": NotRequired[List[SimpleModelTypeDef]],
    },
)

# class ProfileTypeDef(TypedDict):
#     firstname: str
#     lastname: Required[str]
#     phone_number: NotRequired[str]
#     status: ProfileStatusType
#
# class UserTypeDef(TypedDict):
#     user_id: Required[int]
#     profile: Required[ProfileTypeDef]
#     labels: NotRequired[List[str]]
#     tags: Dict[str, str]
