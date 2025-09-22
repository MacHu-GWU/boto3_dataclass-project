# -*- coding: utf-8 -*-

from typing import TypedDict, Required, NotRequired, Optional, Dict, List

from iterals import ProfileStatusType

class SimpleModel(TypedDict):
    attr1: str

class SimpleModelWithSubscript(TypedDict):
    attr1: Required[str]
    attr2: NotRequired[str]
    attr3: List[str]

class SimpleModelWithNestedSubscript(TypedDict):
    attr1: Required[List[str]]
    attr2: NotRequired[List[str]]

class SimpleContainer(TypedDict):
    attr1: SimpleModel
    attr2: Optional[SimpleModel]
    attr3: Required[SimpleModel]
    attr4: NotRequired[SimpleModel]
    attr5: Required[Optional[SimpleModel]]
    attr6: NotRequired[Optional[SimpleModel]]
    attr7: Required[List[SimpleModel]]
    attr8: NotRequired[List[SimpleModel]]

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
