# -*- coding: utf-8 -*-

import textwrap
import dataclasses
from pathlib import Path


def normalize_code(s: str, dedent: bool = True) -> str:
    if dedent:
        s = textwrap.dedent(s)
    return "\n".join(line.rstrip() for line in s.strip().splitlines() if line.rstrip())


def compare_code(
    code: str,
    expected: str,
    dedent: bool = True,
    debug: bool = False,
) -> bool:
    """
    Compares whether two pieces of code are identical, ignoring whitespace and indentation.

    :param code: The generated code string.
    :param expected: The expected code string.

    :return: Returns True if the two code strings are identical after ignoring whitespace and indentation; otherwise, returns False.
    """
    s1 = normalize_code(code, dedent)
    s2 = normalize_code(expected, dedent)
    if debug:
        print(f"--- code ---")
        print(s1)
        print(f"--- expected ---")
        print(s2)
    return s1 == s2


def write(path: Path, content: str):
    """
    Write content to a file, creating parent directories if they do not exist.
    """
    try:
        path.write_text(content, encoding="utf-8")
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


@dataclasses.dataclass
class SemVer:
    """
    Semantic Versioning (SemVer) representation.
    """

    major: int = dataclasses.field()
    minor: int = dataclasses.field()
    patch: int = dataclasses.field()
    dev_id: str | None = dataclasses.field(default=None)

    @property
    def version(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def lower_version(self) -> str:
        return f"{self.major}.{self.minor}.0"

    @property
    def upper_version(self) -> str:
        return f"{self.major}.{self.minor + 1}.0"

    @classmethod
    def parse(cls, s: str):
        parts = s.split(".")
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            return cls(major, minor, patch)
        elif len(parts) == 4:
            major, minor, patch = map(int, parts[:3])
            dev_id = parts[3]
            return cls(major, minor, patch, dev_id)
        else:  # pragma: no cover
            raise ValueError(f"Invalid version string: {s}")
