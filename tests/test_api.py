# -*- coding: utf-8 -*-

from boto3_dataclass import api


def test():
    _ = api


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.api",
        preview=False,
    )
