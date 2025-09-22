# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, List, Dict
import dataclasses
from functools import cached_property

from boto3_dataclass.base import Base

if TYPE_CHECKING:  # pragma: no cover
    import type_defs


@dataclasses.dataclass(frozen=True)
class Profile(Base["type_defs.ProfileTypeDef"]):

    @cached_property
    def firstname(self):
        return self._data["firstname"]

    @cached_property
    def lastname(self):
        return self._data["lastname"]

    @cached_property
    def phone_number(self):
        return self._data.get("phone_number")

    @cached_property
    def status(self):
        return self._data["status"]


@dataclasses.dataclass(frozen=True)
class User(Base["type_defs.UserTypeDef"]):

    @cached_property
    def user_id(self):
        return self._data["user_id"]

    @cached_property
    def profile(self):
        return Profile.new(self._data["profile"])

    @cached_property
    def labels(self):
        return self._data.get("labels", [])

    @cached_property
    def tags(self):
        return self._data["tags"]
