# -*- coding: utf-8 -*-

from boto3_dataclass.structures.boto3_dataclass_service import (
    Boto3DataclassServiceStructure,
)


class TestBoto3DataclassServiceStructure:
    def test(self):
        struct = Boto3DataclassServiceStructure(package_name="boto3_dataclass_iam")

        _ = struct.boto3_stubs_package_name
        _ = struct.boto3_stubs_package_name_slug
        _ = struct.dir_mypy_boto3_package
        _ = struct.path_mypy_boto3_literals_pyi
        _ = struct.path_mypy_boto3_type_defs_pyi
        _ = struct.path_mypy_boto3_client_pyi
        _ = struct.path_boto3_dataclass_type_defs_py
        _ = struct.path_boto3_dataclass_caster_py

        struct_list = Boto3DataclassServiceStructure.list_all()


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.structures.boto3_dataclass_service",
        preview=False,
    )
