# -*- coding: utf-8 -*-

from boto3_dataclass.builders.publish_boto3_dataclass_service import (
    Boto3DataclassServiceBuilder,
)

if __name__ == "__main__":
    Boto3DataclassServiceBuilder.parallel_build_all()
