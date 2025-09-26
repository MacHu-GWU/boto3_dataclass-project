# -*- coding: utf-8 -*-

from boto3_dataclass.pypi import PackageStatusLoader
from rich import print as rprint

package_status_loader = PackageStatusLoader()
package_status_info = package_status_loader.read_cache()
rprint(package_status_info)
