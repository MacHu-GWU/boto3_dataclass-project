# -*- coding: utf-8 -*-

import dataclasses

from ..templates.template_enum import tpl_enum


@dataclasses.dataclass
class CasterMethod:
    method_name: str = dataclasses.field()
    boto3_stubs_type_name: str = dataclasses.field()
    boto3_dataclass_type_name: str = dataclasses.field()

    def gen_code(self) -> str:
        tpl = tpl_enum.boto3_dataclass_service__package__caster_method
        return tpl.render(caster_method=self)


@dataclasses.dataclass
class CasterModule:
    service_name: str = dataclasses.field()
    cms: list[CasterMethod] = dataclasses.field(default_factory=list)

    def gen_code(self) -> str:
        tpl = tpl_enum.boto3_dataclass_service__package__caster_py
        return tpl.render(caster_module=self)
