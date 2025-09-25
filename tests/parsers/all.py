# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.parsers",
        is_folder=True,
        preview=False,
    )
