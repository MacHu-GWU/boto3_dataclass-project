# -*- coding: utf-8 -*-

"""
Use this script to debug
:meth:`boto3_dataclass.builders.publish_boto3_dataclass_service.Boto3DataclassServiceBuilder.parallel_build_all`
"""

from boto3_dataclass.builders.publish_boto3_dataclass_service import (
    Boto3DataclassServiceBuilder,
)

if __name__ == "__main__":
    Boto3DataclassServiceBuilder.parallel_build_all()
    # Boto3DataclassServiceBuilder.parallel_upload_all()
