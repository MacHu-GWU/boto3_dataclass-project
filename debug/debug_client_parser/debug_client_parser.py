# -*- coding: utf-8 -*-

from boto3_dataclass.structures.service import Service
from boto3_dataclass.parsers.client_parser import ClientModuleParser

from rich import print as rprint

service = Service(service_name="ebs")
path_stub_file = service.path_mypy_boto3_client_pyi
print(path_stub_file)
cm_parser = ClientModuleParser(path_stub_file)
cm = cm_parser.parse()
rprint(cm)
