#!/usr/bin/env python3.7
"""--- Day 3: No Matter How You Slice It ---"""
import re
from collections import namedtuple

with open("input_data/day_3") as f:
    data = f.read()

claim_re = r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$"
Claim = namedtuple("Claim", "id x y width height")
claims = [Claim(*map(int, g)) for g in re.findall(claim_re, data, re.M)]

fabric = [[0] * 1000 for _ in range(1000)]
for claim in claims:
    for i in range(claim.y, claim.y + claim.height):
        for j in range(claim.x, claim.x + claim.width):
            fabric[i][j] += 1

n_gt1_claims = sum(x > 1 for row in fabric for x in row)
print(n_gt1_claims, "squares with > 1 claim")

for claim in claims:
    overlaps = set()
    for i in range(claim.y, claim.y + claim.height):
        for j in range(claim.x, claim.x + claim.width):
            overlaps.add(fabric[i][j])

    if len(overlaps) == 1 and 1 in overlaps:
        print("no overlap found at", claim)
