# -*- coding: utf-8 -*-

import dataclasses

import twine.settings

from .runtime import runtime


@dataclasses.dataclass
class Config:
    @property
    def twine_upload_settings(self) -> twine.settings.Settings:
        if runtime.is_github_action:
            raise NotImplementedError
        else:  # is local
            return twine.settings.Settings(
                # repository_name="boto3dataclasspypi", # 🚀 Release to PyPI
                repository_name="boto3dataclasstestpypi",  # 🧪 Release to TestPyPI
                non_interactive=True,
                disable_progress_bar=True,
                skip_existing=True,
            )


config = Config()
