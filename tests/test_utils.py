# -*- coding: utf-8 -*-

from boto3_dataclass.utils import (
    normalize_code,
    compare_code,
    SemVer,
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


class TestSemVer:
    def test(self):
        sem_ver = SemVer.parse("1.40.5")
        assert sem_ver.major == 1
        assert sem_ver.minor == 40
        assert sem_ver.patch == 5
        assert sem_ver.version == "1.40.5"
        assert sem_ver.lower_version == "1.40.0"
        assert sem_ver.upper_version == "1.41.0"

        sem_ver = SemVer.parse("1.40.5.dev1")
        assert sem_ver.major == 1
        assert sem_ver.minor == 40
        assert sem_ver.patch == 5
        assert sem_ver.version == "1.40.5"
        assert sem_ver.lower_version == "1.40.0"
        assert sem_ver.upper_version == "1.41.0"
        assert sem_ver.dev_id == "dev1"


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.utils",
        preview=False,
    )
