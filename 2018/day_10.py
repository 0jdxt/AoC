#!/usr/bin/env python3.7
"""--- Day 10: The Stars Align ---"""
import re


class Point:
    def __init__(self, x, y, vx, vy) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def __repr__(self):
        return f"<Point {self.x},{self.y} ({self.vx},{self.vy})>"


def pmax(points):
    x_max = max(p.x for p in points)
    y_max = max(p.y for p in points)
    return x_max + 1, y_max + 1


def pmin(points):
    x_min = min(p.x for p in points)
    y_min = min(p.y for p in points)
    return x_min, y_min


if __name__ == "__main__":
    regex = r"<(.+),(.+)>.+<(.+),(.+)>"
    with open("input_data/day_10") as f:
        points = [Point(*map(int, x)) for x in re.findall(regex, f.read(), re.M)]

    # move points until height of grid < 50
    t = 0
    while pmax(points)[1] - pmin(points)[1] > 50:
        for point in points:
            point.move()
        t += 1

    # print couple next iterations to visually find message
    for _ in range(4):
        for point in points:
            point.move()

        x_max, y_max = pmax(points)
        x_min, y_min = pmin(points)
        field = [["."] * (x_max - x_min) for _ in range(y_max - y_min)]

        for point in points:
            field[point.y - y_min][point.x - x_min] = "@"

        t += 1
        print(f"    {x_min} -> {x_max}")
        for i, row in enumerate(field):
            print(i + y_min, "".join(row))
        print("tick:", t, "\n")
