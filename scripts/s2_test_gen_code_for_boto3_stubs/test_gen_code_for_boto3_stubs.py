# -*- coding: utf-8 -*-

from pathlib import Path
from boto3_dataclass.gen_code.stub_file import Boto3Stubs
from boto3_dataclass.gen_code.parser import Parser

service = "lambda"
boto3_stubs = Boto3Stubs(service=service)
path_stub_file = boto3_stubs.path_type_def_stub_file
print(path_stub_file)
parser = Parser(path_stub_file=path_stub_file)
tddm = parser.parse()
code = tddm.gen_code(
    type_defs_line=f"from mypy_boto3_{service} import type_defs",
)
dir_here = Path(__file__).absolute().parent
path_generated_module = dir_here / f"aws_{service}.py"
path_generated_module.write_text(code)
