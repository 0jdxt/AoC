#!/usr/bin/env python3.7
"""--- Day 1: Chronal Calibration ---"""
from typing import Set

with open("input_data/day_1") as f:
    data = f.read().splitlines()

top = len(data)
seen_f: Set[int] = set()
freq = i = 0
while freq not in seen_f:
    seen_f.add(freq)
    freq += int(data[i])
    i = (i + 1) % top

print(freq)
