# -*- coding: utf-8 -*-

from boto3_dataclass.pypi import PyPIStatus
from rich import print as rprint

pypi_status = PyPIStatus()
cache_data = pypi_status.read_cache()
rprint(cache_data)
