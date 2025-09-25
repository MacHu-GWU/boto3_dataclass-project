# -*- coding: utf-8 -*-

"""
We use this script to build all ``boto3_dataclass_{service_name}`` package in
``build/repos/`` directory in parallel.
"""

import boto3_dataclass.api as boto3_dc

if __name__ == "__main__":
    boto3_dc.builders.Boto3DataclassServiceBuilder.parallel_build_all()
