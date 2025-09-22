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
    def typed_dict_field(self) -> jinja2.Template:
        return load_template("typed_dict_field.jinja")

    @cached_property
    def typed_dict_def(self) -> jinja2.Template:
        return load_template("typed_dict_def.jinja")

    @cached_property
    def module(self) -> jinja2.Template:
        return load_template("module.jinja")


tpl_enum = TplEnum()
