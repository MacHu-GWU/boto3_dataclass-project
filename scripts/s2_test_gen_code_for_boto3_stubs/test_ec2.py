# -*- coding: utf-8 -*-

from boto3_dataclass.srv.ec2.type_defs import DescribeInstancesResult
# from aws_ec2 import DescribeInstancesResult
from aws_iam import GetRoleResponse
from test_settings import bsm

client = bsm.ec2_client

inst_id = "i-0b040ba7e518d55d7"

res = client.DescribeInstances(InstanceIds=[inst_id])
res = DescribeInstancesResult(res)
print(f"{res. = }")
# print(f"{func.Code = }")
# print(f"{func.Tags = }")
# # print(f"{func.TagsError = }")
# # print(f"{func.Concurrency = }")
# # print(f"{func.ResponseMetadata = }")
