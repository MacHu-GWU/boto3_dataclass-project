# -*- coding: utf-8 -*-

from boto3_dataclass.tests.gen_code.typed_dict_def_mapping import tdm
from pathlib import Path

dir_here = Path(__file__).absolute().parent
path_generated_module = dir_here / "module_2_from_pre_build_type_defs_module.py"
code = tdm.gen_code(
    type_defs_line="from boto3_dataclass.tests.gen_code import type_defs",
)
path_generated_module.write_text(code)
