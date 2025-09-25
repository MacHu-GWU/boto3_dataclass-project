# -*- coding: utf-8 -*-

"""
Use this script to debug
:meth:`boto3_dataclass.builders.publish_boto3_dataclass_service.Boto3DataclassServiceBuilder.build_all`
"""

import boto3_dataclass.api as boto3_dc

from boto3_dataclass._version import __version__

# service_name = "amplifyuibuilder"
# service_name = "ebs"
# service_name = "ec2"
service_name = "iam"
# service_name = "s3"
# service_name = "lambda"
# service_name = "bedrock_runtime"

builder = boto3_dc.builders.Boto3DataclassServiceBuilder(
    version=__version__,
    structure=boto3_dc.structures.Boto3DataclassServiceStructure(
        package_name=f"boto3_dataclass_{service_name}"
    ),
)


if __name__ == "__main__":
    """ """
    builder.log()
    builder.build_all()
    builder.structure.pip_install_editable()
    # builder.structure.poetry_build()
    # builder.structure.twine_upload()
