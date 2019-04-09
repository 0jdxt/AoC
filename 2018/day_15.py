#!/usr/bin/env python3.7
"""--- Day 15: Beverage Bandits ---"""
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, deque


class Point:
    def __init__(self, y, x):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.x},{self.y}>"

    def __sub__(self, other):
        if isinstance(other, Point):
            return abs(self.x - other.x) + abs(self.y - other.y)
        return NotImplemented


class Entity(Point):
    def __init__(self, *args):
        super().__init__(*args)
        self.hp = 200
        self.power = 3

    def __repr__(self):
        return super().__repr__() + f" ({self.hp})"

    def attack(self, other: "Entity"):
        other.hp -= self.power


class Elf(Entity):
    pass


class Goblin(Entity):
    pass


def get_neighbours(p: Point) -> List[Point]:
    return [
        x
        for x in [
            Point(p.y, p.x - 1),
            Point(p.y, p.x + 1),
            Point(p.y + 1, p.x),
            Point(p.y - 1, p.x),
        ]
        if data[x.y][x.x] == "."
    ]


if __name__ == "__main__":
    with open("input_data/day_15") as f:
        data = [list(line.strip()) for line in f]

    # print("\n".join("".join(row) for row in data))

    n_gob = 0
    n_elf = 0
    entities: List[Entity] = []
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char in "#.":
                continue
            if char == "E":
                n_elf += 1
                entities.append(Elf(y, x))
            elif char == "G":
                n_gob += 1
                entities.append(Goblin(y, x))
    entities.sort(key=lambda p: (p.y, p.x))

    # for i in range(50):
    i = 0
    while n_gob and n_elf:
        # def round

        for entity in entities:
            enemies = [e for e in entities if type(e) != type(entity)]
            if not enemies:
                i -= 1
                break
            dists = [entity - e for e in enemies]
            if 1 not in dists:
                possible = []
                for e in enemies:

                    points = get_neighbours(e)
                    if points:
                        m = min(entity - p for p in points)
                        for p in points:
                            r = Point(entity.y, entity.x)
                            delta = True
                            while delta:
                                delta = False
                                if "." in data[r.y]:
                                    r.y += 1
                                    delta = True

                                if any(l[r.x] == "." for l in data):
                                    r.x += 1
                                    delta = True
                            if p - entity == m and p.y < r.y and p.x < r.x:
                                possible.append(p)

                if not possible:
                    # print("no possible moves")
                    continue

                goto = min((p.y, p.x) for p in possible)
                # print(possible, goto)

                start = (entity.y, entity.x)
                frontier = deque([start])
                came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {}
                came_from[start] = None

                # print(entity)
                while len(frontier):
                    curr = frontier.popleft()
                    if curr == goto:
                        break

                    for nxt in get_neighbours(Point(*curr)):
                        tup = (nxt.y, nxt.x)
                        if tup not in came_from:
                            frontier.append(tup)
                            came_from[tup] = curr

                # print(goto, came_from)
                curr = goto
                path = []
                while curr != start:
                    if curr not in came_from:
                        path = []
                        break
                    path.append(curr)
                    curr = came_from[curr]
                # path.append(start)
                # path.reverse()
                if path:
                    data[entity.y][entity.x] = "."
                    step = path[-1]
                    entity.y = step[0]
                    entity.x = step[1]
                    data[entity.y][entity.x] = (
                        "G" if isinstance(entity, Goblin) else "E"
                    )

            dists = [entity - e for e in enemies]
            if 1 in dists:
                enemy = min(
                    (x for x, y in zip(enemies, dists) if y == 1),
                    key=lambda e: (e.hp, e.y, e.x),
                )
                # print(entity, enemy, "->", end=" ")
                entity.attack(enemy)
                if enemy.hp <= 0:
                    if isinstance(enemy, Elf):
                        n_elf -= 1
                    else:
                        n_gob -= 1
                    data[enemy.y][enemy.x] = "."
                # print(enemy.hp)

        entities = list(filter(lambda e: e.hp > 0, entities))
        entities.sort(key=lambda p: (p.y, p.x))
        i += 1

        print("\n".join("".join(row) for row in data))
        print(entities)
    s = sum(e.hp for e in entities)
    print(i, s, s * i)
