#!/usr/bin/env python3.7
"""--- Day 18: Settlers of The North Pole ---"""
from typing import Counter as TCounter, List, Set
from collections import Counter
import time
from tqdm import trange  # type:ignore


def print_grid(grid):
    print("\n".join("".join(row) for row in grid))


def main():
    with open("input_data/day_18") as f:
        data = [list(line.strip()) for line in f]

    rows = len(data)
    cols = len(data[0])
    adj = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not 0 == i == j]

    def get_updates(updates, y, x, acre):
        c: TCounter[str] = Counter()
        for i, j in adj:
            i += x
            j += y
            if not (i < 0 or j < 0 or i >= cols or j >= rows):
                c.update(data[j][i])

        if acre == "." and c["|"] > 2:
            updates.append((y, x, "|"))
        elif acre == "|" and c["#"] > 2:
            updates.append((y, x, "#"))
        elif acre == "#" and not ("#" in c and "|" in c):
            updates.append((y, x, "."))

    seen: Set[int] = set()
    loop: List[int] = []
    with trange(1, 1000) as rng:
        for m in rng:

            updates = []
            for y in range(rows):
                for x, acre in enumerate(data[y]):
                    get_updates(updates, y, x, acre)

            for y, x, ch in updates:
                data[y][x] = ch

            c = Counter()
            for row in data:
                c.update(row)
            res_val = c["|"] * c["#"]

            if res_val in seen:
                if res_val in loop:
                    break
                loop.append(res_val)
            elif loop:
                loop = []
            seen.add(res_val)

    print(f"Found loop after {m} minutes")
    idx = (1_000_000_000 - m) % len(loop)
    print("Resource value after 1,000,000,000 minutes:", loop[idx])


if __name__ == "__main__":
    main()
