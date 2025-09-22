# -*- coding: utf-8 -*-

from typing import Dict, List, Required, NotRequired, TypedDict

from iterals import ProfileStatusType


class ProfileTypeDef(TypedDict):
    firstname: str
    lastname: Required[str]
    phone_number: NotRequired[str]
    status: ProfileStatusType


class UserTypeDef(TypedDict):
    user_id: Required[int]
    profile: Required[ProfileTypeDef]
    labels: NotRequired[List[str]]
    tags: Dict[str, str]
