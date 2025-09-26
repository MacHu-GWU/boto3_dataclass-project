# -*- coding: utf-8 -*-

import dataclasses
from functools import cached_property

import twine.settings

from .runtime import runtime

repo_name_to_api_domain_mapping = {
    "boto3dataclasspypi": "https://pypi.org",
    "boto3dataclasstestpypi": "https://test.pypi.org",
}


@dataclasses.dataclass
class Config:
    repository_name: str = dataclasses.field()

    @cached_property
    def api_domain(self) -> str:
        return repo_name_to_api_domain_mapping[self.repository_name]

    @cached_property
    def twine_upload_settings(self) -> twine.settings.Settings:
        if runtime.is_github_action:
            raise NotImplementedError
        else:  # is local
            return twine.settings.Settings(
                repository_name=self.repository_name,
                non_interactive=True,
                disable_progress_bar=True,
                skip_existing=True,
            )


config = Config(
    repository_name="boto3dataclasspypi", # 🚀 Release to PyPI
    # repository_name="boto3dataclasstestpypi",  # 🧪 Release to TestPyPI
)
