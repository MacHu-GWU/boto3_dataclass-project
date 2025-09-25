# -*- coding: utf-8 -*-

from boto3_dataclass.structures.pyproject import (
    PyProjectStructure,
)


class TestPyProjectStructure:
    def test(self):
        struct = PyProjectStructure(package_name="boto3_dataclass")

        _ = struct.package_name
        _ = struct.package_name_slug
        _ = struct.dir_repo
        _ = struct.dir_package
        _ = struct.path_pyproject_toml
        _ = struct.path_README_rst
        _ = struct.path_LICENSE_txt
        _ = struct.path_init_py

        try:
            _ = struct.dist_files
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.structures.pyproject",
        preview=False,
    )
