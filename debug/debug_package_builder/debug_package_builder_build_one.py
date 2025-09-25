# -*- coding: utf-8 -*-

import boto3_dataclass.api as boto3_dc

# from boto3_dataclass.structures.service import Service
# from boto3_dataclass.publish.builder import PackageBuilder
from boto3_dataclass._version import __version__
from boto3_dataclass.paths import path_enum
from boto3_dataclass.vendor.better_pathlib import temp_cwd

# service_name = "amplifyuibuilder"
# service_name = "ebs"
# service_name = "ec2"
service_name = "iam"

package = boto3_dc.publish.PackageBuilder(
    service=boto3_dc.structures.Service(service_name=service_name),
    version=__version__,
)


if __name__ == "__main__":
    """ """
    package.log()
    package.build_all()
    package.poetry_build()
    package.pip_install_editable()

    # package.twine_upload()

    # Sample usage after installation
    # import typing as T
    # from boto3_dataclass_iam import iam_caster
    #
    # if T.TYPE_CHECKING:  # pragma: no cover
    #     from mypy_boto3_iam import IAMClient
    #
    # iam_client: IAMClient = ...
    # res = iam_client.get_role(RoleName="my-role")
    # res = iam_caster.get_role(res)
    # _ = res.Role.Arn  # type hint works
