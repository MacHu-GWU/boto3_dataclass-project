# -*- coding: utf-8 -*-

"""

"""
import mpire
from boto3_dataclass.gen_code.stub_file import Boto3Stubs


def main(ith: int, boto3_stubs: Boto3Stubs):
    print(f"========== {ith} {boto3_stubs.service} ==========")
    boto3_stubs.write_code()


if __name__ == "__main__":
    n_workers = None
    boto3_stubs_list = Boto3Stubs.list_all()
    tasks = [
        {"ith": i, "boto3_stubs": boto3_stubs}
        for i, boto3_stubs in enumerate(boto3_stubs_list, start=1)
    ]
    with mpire.WorkerPool(n_jobs=n_workers, start_method="fork") as pool:
        results = pool.map(main, tasks)
