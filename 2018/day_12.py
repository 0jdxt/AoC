#!/usr/bin/env python3.7
"""--- Day 12: Subterranean Sustainability ---"""
from collections import defaultdict

if __name__ == "__main__":

    with open("input_data/day_12") as f:
        initial = f.readline().strip().split(": ")[1]
        f.readline()
        data = [line.strip().split(" => ") for line in f]

    def no_plant():
        return "."

    rules = defaultdict(no_plant, {x[0]: x[1] for x in data})

    def sum_at_gen(state, n):
        last_s, last_d = sum(state.keys()), 0
        for gen in range(n):
            min_i = min(state.keys()) - 2
            max_i = max(state.keys()) + 3

            state = defaultdict(
                no_plant,
                {
                    i: "#"
                    for i in range(min_i, max_i)
                    if rules["".join(state[j] for j in range(i - 2, i + 3))] == "#"
                },
            )

            s = sum(state.keys())
            d = s - last_s

            # print(
            #     f"{gen+1:3} {min_i:3}",
            #     "".join(state[x] if x in state else "." for x in range(min_i, max_i)),
            # )

            if d - last_d == 0 and d == 58:
                return (n - gen - 1) * d + s
            last_s, last_d = s, d
        return last_s

    state = defaultdict(no_plant, {i: c for i, c in enumerate(initial) if c == "#"})

    # print(f" 0 .....{initial}")
    print(sum_at_gen(state, 20))
    print(sum_at_gen(state, 50_000_000_000))
