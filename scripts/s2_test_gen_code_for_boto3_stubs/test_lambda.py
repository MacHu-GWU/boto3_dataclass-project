# -*- coding: utf-8 -*-

from aws_lambda import GetFunctionResponse
from test_settings import bsm

client = bsm.lambda_client

func_name = "aws_bedrock_agent_workflow_poc-dev-baacco"

res = client.get_function(FunctionName=func_name)
func = GetFunctionResponse(res)
print(f"{func.Configuration = }")
print(f"{func.Code = }")
print(f"{func.Tags = }")
# print(f"{func.TagsError = }")
# print(f"{func.Concurrency = }")
# print(f"{func.ResponseMetadata = }")
