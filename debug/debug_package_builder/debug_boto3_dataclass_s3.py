# -*- coding: utf-8 -*-

from boto3_dataclass_s3 import s3_caster

from boto3_dataclass.tests.aws import bsm
from rich import print as rprint

s3_client = bsm.s3_client
res = s3_client.list_buckets()
res = s3_caster.list_buckets(res)
_ = res.Buckets[0].Name # type hint works

res = s3_client.head_bucket(Bucket=res.Buckets[0].Name)
res = s3_caster.head_bucket(res)
_ = res.BucketRegion  # type hint works
rprint(res.BucketRegion)
print(f"{res.ResponseMetadata.RequestId = }")
rprint(f"{res.BucketRegion = }")
