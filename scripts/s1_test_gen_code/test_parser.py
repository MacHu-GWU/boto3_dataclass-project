# -*- coding: utf-8 -*-

from boto3_dataclass.gen_code.parser import Parser
from boto3_dataclass.paths import dir_package

path_stub_file = dir_package / "tests" / "gen_code" / "type_defs.pyi"
parser = Parser(path_stub_file=path_stub_file)
parser.parse()

