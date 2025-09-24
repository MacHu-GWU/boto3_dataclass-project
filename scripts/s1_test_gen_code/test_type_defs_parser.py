# -*- coding: utf-8 -*-

from boto3_dataclass.gen_code.type_defs_parser import TypedDictDefMappingParser

from boto3_dataclass.paths import path_test_stub_file
from pathlib import Path

tddm_parser = TypedDictDefMappingParser(path_stub_file=path_test_stub_file)
tddm = tddm_parser.parse()

dir_here = Path(__file__).absolute().parent
path_generated_module = dir_here / f"module_parse_then_generated.py"

code = tddm.gen_code(
    type_defs_line="from boto3_dataclass.tests.gen_code import type_defs",
)
path_generated_module.write_text(code)
