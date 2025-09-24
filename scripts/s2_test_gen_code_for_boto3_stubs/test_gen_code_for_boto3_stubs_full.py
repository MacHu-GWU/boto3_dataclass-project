# -*- coding: utf-8 -*-

from boto3_dataclass.gen_code.stub_file import Boto3Stubs

boto3_stubs_list = Boto3Stubs.list_all()

for i, boto3_stubs in enumerate(boto3_stubs_list, start=1):
    print(f"========== {i} {boto3_stubs.service} ==========")
    boto3_stubs.write_code()
