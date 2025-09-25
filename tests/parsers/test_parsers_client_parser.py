# -*- coding: utf-8 -*-

from boto3_dataclass.parsers.client_parser import ClientModuleParser
from boto3_dataclass.structures.boto3_dataclass_service import (
    Boto3DataclassServiceStructure,
)


class TestTypedDefsModuleParser:
    def test_parse(self):
        struct = Boto3DataclassServiceStructure(package_name="boto3_dataclass_iam")
        cm_parser = ClientModuleParser(
            path_stub_file=struct.path_mypy_boto3_client_pyi,
        )
        cm = cm_parser.parse()

        caster_method = cm.cms_mapping["get_role"]
        assert caster_method.method_name == "get_role"
        assert caster_method.boto3_stubs_type_name == "GetRoleResponseTypeDef"
        assert caster_method.boto3_dataclass_type_name == "GetRoleResponse"


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.parsers.client_parser",
        preview=False,
    )
