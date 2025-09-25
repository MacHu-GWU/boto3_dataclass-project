# -*- coding: utf-8 -*-

"""
Use this script to debug the ``boto3_dataclass.builders.publish_boto3_dataclass.Boto3DataclassBuilder``.
"""

import boto3_dataclass.api as boto3_dc

builder = boto3_dc.builders.Boto3DataclassBuilder.new()


if __name__ == "__main__":
    """ """
    builder.log()
    builder.build_all()
    # builder.structure.pip_install_editable()
    # builder.structure.poetry_build()
    # builder.structure.twine_upload()
