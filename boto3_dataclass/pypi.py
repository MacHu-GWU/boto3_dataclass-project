# -*- coding: utf-8 -*-

import json
import requests
import dataclasses
from pathlib import Path
from functools import cached_property

from rich import print as rprint

from ._version import __version__
from .paths import path_enum
from .utils import write
from .config import config

from .structures.api import Boto3DataclassServiceStructure


@dataclasses.dataclass
class PyPIStatus:
    version: str = dataclasses.field(default=__version__)

    @cached_property
    def path_cache_file(self) -> Path:
        return path_enum.dir_cache / f"{self.version}.json"


def get_project(name: str):
    # url = f"{domain}/pypi/{name}/json"
    url = f"{domain}/simple/{name}/"
    headers = {"Accept": "application/vnd.pypi.simple.v1+json"}
    res = requests.get(url, headers=headers)
    rprint(res.json())


name = "boto3-dataclass-iam"
get_project(name)
