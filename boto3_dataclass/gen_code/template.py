# -*- coding: utf-8 -*-

from pathlib import Path
from functools import cached_property

import jinja2

dir_here = Path(__file__).absolute().parent
dir_tpl = dir_here / "tpl"


def load_template(name: str) -> jinja2.Template:
    path = dir_tpl / name
    return jinja2.Template(path.read_text(encoding="utf-8"))


class TplEnum:
    @cached_property
    def path(self) -> jinja2.Template:
        return load_template("abc.md")


tpl_enum = TplEnum()
