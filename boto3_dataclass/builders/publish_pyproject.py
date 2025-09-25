# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from functools import cached_property

from jinja2 import Template

from ..utils import write, SemVer


@dataclasses.dataclass
class PyProjectBuilder:
    version: str = dataclasses.field()

    @cached_property
    def sem_ver(self) -> SemVer:
        return SemVer.parse(self.version)

    def build_by_template(
        self,
        path: Path,
        template: Template,
    ):
        code = template.render(builder=self)
        write(path, code)
