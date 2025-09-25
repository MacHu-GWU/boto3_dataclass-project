# -*- coding: utf-8 -*-

from boto3_dataclass.publish.builder import PackageBuilder

__version__ = "0.1.1"

if __name__ == "__main__":
    PackageBuilder.parallel_build_all(version=__version__)
