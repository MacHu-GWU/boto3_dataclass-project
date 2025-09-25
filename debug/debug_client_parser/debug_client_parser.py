# -*- coding: utf-8 -*-

from boto3_dataclass.structures.boto3_dataclass_service import (
    Boto3DataclassServiceStructure,
)
from boto3_dataclass.parsers.client_parser import ClientModuleParser

from rich import print as rprint

service_name = "ebs"
struct = Boto3DataclassServiceStructure(package_name=f"boto3_dataclass_{service_name}")
path_stub_file = struct.path_mypy_boto3_client_pyi
print(path_stub_file)
cm_parser = ClientModuleParser(path_stub_file)
cm = cm_parser.parse()
rprint(cm)
