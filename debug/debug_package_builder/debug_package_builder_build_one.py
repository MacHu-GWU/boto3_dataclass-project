# -*- coding: utf-8 -*-

from boto3_dataclass.structures.service import Service
from boto3_dataclass.publish.builder import PackageBuilder

# service_name = "ebs"
# service_name = "ec2"
service_name = "amplifyuibuilder"

__version__ = "0.1.1"

package = PackageBuilder(
    service=Service(service_name=service_name),
    version=__version__,
)
package.build_all()
