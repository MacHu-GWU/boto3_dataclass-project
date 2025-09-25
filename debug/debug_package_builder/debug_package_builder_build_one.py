# -*- coding: utf-8 -*-

from boto3_dataclass.structures.service import Service
from boto3_dataclass.publish.builder import PackageBuilder
from boto3_dataclass.paths import path_enum
from pathlib_mate import Path
import subprocess

# service_name = "amplifyuibuilder"
# service_name = "ebs"
# service_name = "ec2"
service_name = "iam"

__version__ = "0.1.1"

package = PackageBuilder(
    service=Service(service_name=service_name),
    version=__version__,
)


def pip_install():
    dir_repo = Path(package.service.dir_boto3_dataclass_repo)
    args = [f"{path_enum.dir_venv_bin / 'pip'}", "install", "-e", "."]
    with dir_repo.temp_cwd():
        subprocess.run(args)


if __name__ == "__main__":
    """ """
    package.log()
    package.build_all()
    # pip_install()

    from boto3_dataclass_iam.type_defs import GetRoleResponse
