# -*- coding: utf-8 -*-

import json
import dataclasses
from pathlib import Path
from functools import cached_property

import asyncio

from ._version import __version__
from .paths import path_enum
from .utils import write
from .config import config

from .structures.api import Boto3DataclassServiceStructure
from .async_http import fetch_all_urls


def make_url(domain: str, package: str, version: str) -> str:
    return f"{domain}/pypi/{package}/{version}/json"


def extract_package_name_from_url(url: str) -> str:
    parts = url.split("/")
    return parts[-3]


T_PACKAGE_STATUS_INFO = dict[str, bool]


@dataclasses.dataclass
class PackageStatusLoader:
    version: str = dataclasses.field(default=__version__)

    @cached_property
    def path_cache_file(self) -> Path:
        return path_enum.dir_cache / f"{self.version}.json"

    def read_cache(self) -> T_PACKAGE_STATUS_INFO:
        path = self.path_cache_file
        if path.exists() is False:
            return self.refresh_cache()
        return json.loads(path.read_text(encoding="utf-8"))

    def refresh_cache(self) -> T_PACKAGE_STATUS_INFO:
        results = asyncio.run(self.fetch_package_infos())
        cache_data = {}
        for result in results:
            package = extract_package_name_from_url(result.url)
            if result.error is not None:
                is_exists = False
            else:
                is_exists = "info" in result.response.json()
            cache_data[package] = is_exists
        content = json.dumps(cache_data, indent=2)
        path = self.path_cache_file
        write(path, content)
        return cache_data

    async def fetch_package_infos(self):
        urls = self.urls
        results = await fetch_all_urls(urls)
        return results

    @cached_property
    def urls(self) -> list[str]:
        struct_list = Boto3DataclassServiceStructure.list_all()
        urls = [
            make_url(
                domain=config.api_domain,
                package=struct.package_name_slug,
                version=self.version,
            )
            for struct in struct_list
        ]
        return urls
