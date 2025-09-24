# -*- coding: utf-8 -*-

from boto3_dataclass.utils import normalize_code


def test_normalize_code():
    s = "\n".join(
        [
            "class User:",
            "",
            "    def __init__(self, id: int, name: str):",
            "        self.id = id  ",
            "        self.name = name",
        ]
    )
    s1 = normalize_code(s)
    expected = "\n".join(
        [
            "class User:",
            "    def __init__(self, id: int, name: str):",
            "        self.id = id",
            "        self.name = name",
        ]
    )
    assert s1 == expected


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.utils",
        preview=False,
    )
