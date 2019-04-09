#!/usr/bin/env python3.7
"""--- Day 6: Chronal Coordinates ---"""
from typing import List, Tuple, Dict, Set
from collections import defaultdict
import re
import string


def main() -> None:
    with open("input_data/day_6") as f:
        data = f.read()
    coord_re = re.compile(r"^(\d+), (\d+)$", re.M)
    coords = [(int(x), int(y)) for x, y in coord_re.findall(data)]

    min_x = min(coords)[0]
    max_x = max(coords)[0] + 1
    min_y = min(coords, key=lambda x: x[1])[1]
    max_y = max(coords, key=lambda x: x[1])[1] + 1

    # create grid
    letters = list(string.ascii_letters)
    grid = [[" "] * max_x for _ in range(max_y)]
    within_10k = 0
    for i in range(min_y, max_y):
        for j in range(min_x, max_x):
            dists = list(map(lambda c: abs(c[0] - j) + abs(c[1] - i), coords))

            # Part 1
            min_dist = min(dists)
            n_closest = sum(x == min_dist for x in dists)
            grid[i][j] = letters[dists.index(min_dist)] if n_closest == 1 else "."

            # Part 2
            within_10k += int(sum(dists) < 1e4)

    print(within_10k, "squares are within 10k units of all stars")

    # count areas
    infs: Set[str] = set(".")  # ignore equi-distant pts
    d: Dict[str, int] = defaultdict(int)
    for i in range(min_y, max_y):
        for j in range(min_x, max_x):
            val = grid[i][j]

            # Part 1
            if val in infs:
                continue

            if i <= min_y or j <= min_x or i >= max_y - 1 or j >= max_x - 1:
                infs.add(val)
                if val in d:
                    del d[val]
            else:
                d[val] += 1

    best_star = max(d, key=d.get)
    print("Most isolated star:", best_star, d[best_star], "squares")


if __name__ == "__main__":
    main()
