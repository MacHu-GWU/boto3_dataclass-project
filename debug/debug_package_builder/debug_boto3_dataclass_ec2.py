# -*- coding: utf-8 -*-

from boto3_dataclass_ec2 import ec2_caster

from boto3_dataclass.tests.aws import bsm
from rich import print as rprint

ec2_client = bsm.ec2_client
res = ec2_client.describe_instances()
res = ec2_caster.describe_instances(res)

rprint(res)
inst = res.Reservations[0].Instances[0]
print(f"{inst.InstanceId = }")
print(f"{inst.ImageId = }")
print(f"{inst.State.Name = }")
