# -*- coding: utf-8 -*-


def normalize_code(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines() if line.rstrip())


def compare_code(code: str, expected: str) -> bool:
    """
    Compares whether two pieces of code are identical, ignoring whitespace and indentation.

    :param code: The generated code string.
    :param expected: The expected code string.

    :return: Returns True if the two code strings are identical after ignoring whitespace and indentation; otherwise, returns False.
    """
    return normalize_code(code) == normalize_code(expected)
