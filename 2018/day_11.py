#!/usr/bin/env python3.7
"""--- Day 11: Chronal Charge ---"""
from functools import lru_cache


@lru_cache(maxsize=None)
def get_power_at(rack_id, y, serial):
    m = (rack_id * y + serial) * rack_id
    return ((m // 100) % 10) - 5


def most_power(serial, sq_size):
    squares = []
    for x in range(1, 301 - sq_size - (300 % sq_size)):
        for y in range(1, 301 - sq_size - (300 % sq_size)):
            tot = sum(
                get_power_at(x + m + 10, y + n, serial)
                for m in range(sq_size)
                for n in range(sq_size)
            )
            squares.append((tot, x, y))
    return "Power %d found at %d,%d" % max(squares)


if __name__ == "__main__":
    serial = 8868
    print(most_power(serial, 12))
