# -*- coding: utf-8 -*-

from boto3_dataclass.gen_code.type_defs_parser import TypedDictDefMappingParser
from boto3_dataclass.paths import dir_package, dir_unit_test

path_stub_file = dir_package / "tests" / "gen_code" / "type_defs.pyi"
path_generated_module = dir_unit_test / "gen_code" / "module_parsed_then_generated.py"


class TestTypedDictDefMappingParser:
    def test_parse(self):
        parser = TypedDictDefMappingParser(path_stub_file=path_stub_file)
        tddm = parser.parse()
        code = tddm.gen_code(
            type_defs_line="from boto3_dataclass.tests.gen_code import type_defs",
        )
        path_generated_module.write_text(code)


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.gen_code.type_defs_parser",
        preview=False,
    )
