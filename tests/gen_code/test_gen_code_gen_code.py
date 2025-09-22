# -*- coding: utf-8 -*-

from boto3_dataclass.tests.gen_code.typed_dict_def_mapping import tddm
from boto3_dataclass.paths import dir_unit_test

path_generated_module = dir_unit_test / "gen_code" / f"module_generated.py"


class TestTypedDictDefMapping:
    def test_gen_code(self):
        code = tddm.gen_code(
            type_defs_line="from boto3_dataclass.tests.gen_code import type_defs",
        )
        path_generated_module.write_text(code)


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.gen_code.gen_code",
        preview=False,
    )
