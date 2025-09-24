# -*- coding: utf-8 -*-

import textwrap


def normalize_code(s: str, dedent: bool = True) -> str:
    if dedent:
        s = textwrap.dedent(s)
    return "\n".join(line.rstrip() for line in s.strip().splitlines() if line.rstrip())


def compare_code(
    code: str,
    expected: str,
    dedent: bool = True,
) -> bool:
    """
    Compares whether two pieces of code are identical, ignoring whitespace and indentation.

    :param code: The generated code string.
    :param expected: The expected code string.

    :return: Returns True if the two code strings are identical after ignoring whitespace and indentation; otherwise, returns False.
    """
    return normalize_code(code, dedent) == normalize_code(expected, dedent)
