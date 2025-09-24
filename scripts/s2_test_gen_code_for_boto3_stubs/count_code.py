# -*- coding: utf-8 -*-

"""
- 413 Services
- 1892086 lines
- 76 MB
"""
from pathlib import Path

def count_file(p: Path):
    return len(p.read_text().splitlines())

def count_all():
    dir = Path("/Users/sanhehu/Documents/GitHub/boto3_dataclass-project/boto3_dataclass/srv")
    total = 0
    pairs = list()
    for p in dir.rglob("*.py"):
        service = p.parent.name
        n = count_file(p)
        pair = (service, n)
        pairs.append(pair)
        total += n

    pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    for service, n in pairs:
        print(f"{service:30} {n:6}")
    print(f"Total: {total} lines")
    print(f"Number of service: {len(pairs)}")

count_all()