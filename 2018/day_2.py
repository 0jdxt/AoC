#!/usr/bin/env python3.7
"""--- Day 2: Inventory Management System ---"""
from typing import Set
from collections import Counter

with open("input_data/day_2") as f:
    data = f.read().splitlines()

twos = threes = 0
for box_id in data:
    c = Counter(box_id)
    twos += int(2 in c.values())
    threes += int(3 in c.values())
print(f"checksum: {twos * threes}")

lowest = len(data)
ids: Set[str] = set()
for i, ref in enumerate(data):
    for oth in data[i + 1 :]:
        n_diff = sum(x != y for x, y in zip(ref, oth))

        if n_diff < lowest:
            lowest = n_diff
            ids.clear()
        if n_diff <= lowest:
            ids |= set([ref, oth])

print("closest IDs:")
for bid in ids:
    print(bid)

if len(ids) == 2:
    print("common letters:\n" + "".join(m for m, n in zip(*ids) if m == n))
