#!/usr/bin/env python3.7
"""--- Day 13: Mine Cart Madness ---"""
from typing import List
from itertools import cycle
from copy import deepcopy


class Cart:
    __slots__ = ("char", "x", "y", "_turn")
    dir_map = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}
    dirs = {"^": "<^>", ">": "^>v", "v": ">v<", "<": "v<^"}
    turns = {
        "\\": {"<": "^", "^": "<", "v": ">", ">": "v"},
        "/": {"v": "<", "<": "v", ">": "^", "^": ">"},
    }

    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self._turn = cycle(range(3))

    def move(self):
        v = self.dir_map[self.char]
        self.x += v[0]
        self.y += v[1]

    def turn(self, track):
        self.char = self.turns[track][self.char]

    def inter(self):
        self.char = self.dirs[self.char][next(self._turn)]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'<Cart "{self.char}" {self.x},{self.y}>'


if __name__ == "__main__":
    with open("input_data/day_13") as f:
        tracks = [list(line.strip("\n")) for line in f]

    carts = []
    for y, row in enumerate(tracks):
        for x, char in enumerate(row):
            if char in Cart.dirs:
                carts.append(Cart(char, x, y))
                tracks[y][x] = "-" if char in "<>" else "|"

    while len(carts) > 1:
        carts.sort(key=lambda c: (c.y, c.x))
        # temp = deepcopy(tracks)
        seen: List[Cart] = []
        for i, cart in enumerate(carts):
            cart.move()

            if cart in seen:
                seen.remove(cart)
                print(f"collision at {cart.x:3},{cart.y:3}")
                continue
            elif cart in carts[i + 1 :]:
                carts.remove(cart)
                print(f"collision at {cart.x:3},{cart.y:3}")
                continue

            track = tracks[cart.y][cart.x]
            if track == "+":
                cart.inter()
            elif track in Cart.turns:
                cart.turn(track)

            # temp[cart.y][cart.x] = cart.char

            seen.append(cart)
        carts = seen

        # print(carts)
        # for row in temp:
        #     print("".join(row))

    print("last cart:", carts[0])
