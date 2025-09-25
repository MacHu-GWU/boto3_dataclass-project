# -*- coding: utf-8 -*-

"""
Use this script to debug the ``boto3_dataclass.publish.builder.PackageBuilder``
"""

import boto3_dataclass.api as boto3_dc

from boto3_dataclass._version import __version__

# service_name = "amplifyuibuilder"
# service_name = "ebs"
# service_name = "ec2"
# service_name = "iam"
# service_name = "s3"
# service_name = "lambda"
service_name = "bedrock_runtime"

package = boto3_dc.publish.PackageBuilder(
    service=boto3_dc.structures.Service(service_name=service_name),
    version=__version__,
)


if __name__ == "__main__":
    """ """
    package.log()
    package.build_all()
    package.pip_install_editable()
    # package.poetry_build()
    # package.twine_upload()
