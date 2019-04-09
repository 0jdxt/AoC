#!/usr/bin/env python3.7
"""--- Day 5: Alchemical Reduction ---"""
import string
import sys


def react(poly: str) -> str:
    count = 1
    while count:
        i, count, new, top = 1, 0, "", len(poly)
        while i < top:
            a, b = poly[i - 1], poly[i]
            if a.isupper() ^ b.isupper() and (a == b.lower() or b == a.lower()):
                i += 1
                count += 1
            else:
                new += a
            i += 1
        poly = new + b
    return poly


def main() -> None:
    with open("input_data/day_5") as f:
        data = f.read().strip()

    x = "dabAcCaCBAcCcaDA"
    print(f'test react "{x}":', react(x))

    print("\nReacting actual polymer...")
    print(len(data), "->", end=" ")
    reacted = react(data)
    print(len(reacted))

    print("\nFinding problematic unit type...\ncompleted: ", end="")
    lowest = len(data), ""
    for char in string.ascii_lowercase:
        sys.stdout.write(char)
        sys.stdout.flush()
        filt = data.replace(char, "").replace(char.upper(), "")
        lowest = min((len(react(filt)), char), lowest)
    print(f"\nLowest: {lowest[1]}/{lowest[1].upper()} -> {lowest[0]}")


if __name__ == "__main__":
    main()
