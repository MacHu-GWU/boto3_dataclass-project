# -*- coding: utf-8 -*-

from boto3_dataclass.parsers.type_defs_parser import TypedDefsModuleParser
from pathlib import Path
from rich import print as rprint

dir_here = Path(__file__).absolute().parent
path_stub_file = dir_here / "module.pyi"

tdm_parser = TypedDefsModuleParser(path_stub_file)
tdm = tdm_parser.parse()
rprint(tdm)