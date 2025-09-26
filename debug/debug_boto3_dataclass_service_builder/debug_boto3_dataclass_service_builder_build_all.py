# -*- coding: utf-8 -*-

"""
Use this script to debug
:meth:`boto3_dataclass.builders.publish_boto3_dataclass_service.Boto3DataclassServiceBuilder.parallel_build_all`
"""

from boto3_dataclass.builders.publish_boto3_dataclass_service import (
    Boto3DataclassServiceBuilder,
)
from boto3_dataclass.pypi import PackageStatusLoader

if __name__ == "__main__":
    package_status_loader = PackageStatusLoader()
    package_status_info = package_status_loader.read_cache()
    # package_status_info = None

    limit = None
    # limit = 3

    # fmt: off
    Boto3DataclassServiceBuilder.parallel_build_all(package_status_info=package_status_info, limit=limit)
    # Boto3DataclassServiceBuilder.parallel_upload_all(package_status_info=package_status_info, limit=limit)
    # fmt: on
