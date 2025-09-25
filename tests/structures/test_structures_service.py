# -*- coding: utf-8 -*-

from boto3_dataclass.structures.service import (
    Service,
)


class TestService:
    def test(self):
        service = Service(service_name="iam")
        _ = service.boto3_stubs_package_name
        _ = service.boto3_stubs_package_name_slug
        _ = service.dir_mypy_boto3_package
        _ = service.path_mypy_boto3_literals_pyi
        _ = service.path_mypy_boto3_type_defs_pyi
        _ = service.path_mypy_boto3_client_pyi
        _ = service.boto3_dataclass_package_name
        _ = service.boto3_dataclass_package_name_slug
        _ = service.dir_boto3_dataclass_repo
        _ = service.dir_boto3_dataclass_package
        _ = service.path_boto3_dataclass_pyproject_toml
        _ = service.path_boto3_dataclass_README_rst
        _ = service.path_boto3_dataclass_init_py
        _ = service.path_boto3_dataclass_type_defs_py
        _ = service.path_boto3_dataclass_caster_py

        try:
            _ = service.dist_files
        except FileNotFoundError:
            pass

        service_list = Service.list_all()


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.structures.service",
        preview=False,
    )
