# -*- coding: utf-8 -*-

"""
We use this script to build all ``boto3_dataclass_{service_name}`` package in
``build/repos/`` directory in parallel.
"""

import boto3_dataclass.api as boto3_dc
from boto3_dataclass._version import __version__

if __name__ == "__main__":
    boto3_dc.publish.PackageBuilder.parallel_build_all(version=__version__)
