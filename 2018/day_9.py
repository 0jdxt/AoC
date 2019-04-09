#!/usr/bin/env python3.7
"""--- Day 9: Marble Mania ---"""
from collections import deque
from itertools import cycle
from timeit import Timer as T


def main(n_players: int, n_marbles: int) -> int:
    circle = deque([0])
    players = {i: 0 for i in range(n_players)}
    for p, m in zip(cycle(players), range(1, n_marbles + 1)):
        if m % 23:
            circle.rotate(2)
            circle.append(m)
        else:
            circle.rotate(-7)
            players[p] += m + circle.pop()
    return players[max(players, key=players.get)]


if __name__ == "__main__":
    data = "459 players; last marble is worth 72103".split()
    n_players = int(data[0])
    n_marbles = int(data[6])
    # print(n_players, "players,", n_marbles, "marbles")
    print(data)

    print(main(n_players, n_marbles))
    print(T(lambda: main(n_players, n_marbles)).timeit(1))

    print(main(n_players, n_marbles * 100))
    print(T(lambda: main(n_players, n_marbles * 100)).timeit(1))
