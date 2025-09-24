# -*- coding: utf-8 -*-

from boto3_dataclass.utils import (
    normalize_code,
    compare_code,
)


def test_normalize_code():
    # case 1
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


def test_compare_code():
    s = "\n".join(
        [
            "    def __init__(self, id: int, name: str):",
            "        self.id = id  ",
            "        self.name = name",
        ]
    )
    s1 = """
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    """
    assert compare_code(s, s1) is True


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.utils",
        preview=False,
    )
