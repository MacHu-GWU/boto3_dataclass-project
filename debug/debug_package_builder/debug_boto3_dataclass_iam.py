# -*- coding: utf-8 -*-

from boto3_dataclass_iam import iam_caster

from boto3_dataclass.tests.aws import bsm
from rich import print as rprint

iam_client = bsm.iam_client
res = iam_client.list_roles()
res = iam_caster.list_roles(res)
_ = res.Roles[0].RoleName # type hint works

res = iam_client.get_role(RoleName=res.Roles[0].RoleName)
res = iam_caster.get_role(res)
_ = res.Role.Arn  # type hint works
rprint(res)
rprint(res.Role)
print(f"{res.ResponseMetadata.RequestId = }")
