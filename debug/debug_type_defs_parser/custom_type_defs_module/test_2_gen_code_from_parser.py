# -*- coding: utf-8 -*-

from boto3_dataclass.parsers.type_defs_parser import TypedDefsModuleParser
from boto3_dataclass.paths import path_enum
from pathlib import Path

dir_here = Path(__file__).absolute().parent
path_generated_module = dir_here / "module_3_from_parser.py"

parser = TypedDefsModuleParser(path_stub_file=path_enum.path_test_stub_file)
tddm = parser.parse()
code = tddm.gen_code(
    type_defs_line="from boto3_dataclass.tests.gen_code import type_defs",
)
path_generated_module.write_text(code)
