# -*- coding: utf-8 -*-

from boto3_dataclass.parsers.type_defs_parser import TypedDefsModuleParser
from boto3_dataclass.structures.service import (
    Service,
)


class TestTypedDefsModuleParser:
    def test_parse(self):
        service = Service(service_name="iam")
        tdm_parser = TypedDefsModuleParser(
            path_stub_file=service.path_mypy_boto3_type_defs_pyi,
        )
        tdm = tdm_parser.parse()

        tdd = tdm.tdds_mapping["GetRoleResponseTypeDef"]
        tdf = tdd.fields_mapping["Role"]
        assert tdf.name == "Role"
        assert tdf.anno.is_nested_typed_dict is True
        assert tdf.anno.nested_type_name == "RoleTypeDef"
        assert tdf.anno.nested_type_subscriptor == "NULL"

        tdd = tdm.tdds_mapping["ListRolesResponseTypeDef"]
        tdf = tdd.fields_mapping["Roles"]
        assert tdf.name == "Roles"
        assert tdf.anno.is_nested_typed_dict is True
        assert tdf.anno.nested_type_name == "RoleTypeDef"
        assert tdf.anno.nested_type_subscriptor == "List"


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.parsers.type_defs_parser",
        preview=False,
    )
