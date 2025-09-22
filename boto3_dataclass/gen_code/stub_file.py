# -*- coding: utf-8 -*-

import site
import dataclasses
from functools import cached_property
from pathlib import Path

dir_site_packages = Path(site.getsitepackages()[0])


@dataclasses.dataclass
class Boto3Stubs:
    """
    :param name: The name of the AWS Service or module.
    """

    service: str = dataclasses.field()

    @cached_property
    def path_type_def_stub_file(self) -> Path:
        """
        Get the path to the type definition stub file (type_defs.pyi) for a given package or module name.
        """
        folder = f"mypy_boto3_{self.service}"
        return dir_site_packages.joinpath(folder, "type_defs.pyi")
