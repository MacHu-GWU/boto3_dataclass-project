# -*- coding: utf-8 -*-

from boto3_dataclass_lambda import lambda_caster

from boto3_dataclass.tests.aws import bsm
from rich import print as rprint

lambda_client = bsm.lambda_client
res = lambda_client.list_functions()
res = lambda_caster.list_functions(res)
_ = res.Functions[0].FunctionName # type hint works

res = lambda_client.get_function(FunctionName=res.Functions[0].FunctionName)
res = lambda_caster.get_function(res)
_ = res.Configuration.Role  # type hint works
rprint(res)
rprint(f"{res.Configuration.Role = }")
print(f"{res.ResponseMetadata.RequestId = }")
