#!/usr/bin/env python3.7
"""--- Day 7: The Sum of Its Parts ---"""
from typing import Set, Dict, List, Tuple, Deque
from collections import defaultdict, namedtuple, deque
from bisect import insort
import re
import string
from timeit import Timer as T


class Node:
    __slots__ = ("after", "before")

    def __init__(self) -> None:
        self.after: Set[str] = set()
        self.before: Set[str] = set()

    def __repr__(self) -> str:
        return f"<Node {self.before} {self.after}>"


def do(d: Dict[str, Node], dur: Dict[str, int], n_workers: int = 1) -> Tuple[str, int]:
    stack = deque(sorted(x for x, y in d.items() if not len(y.before)))
    proc = ""
    t = -1
    workers: Deque[Tuple[str, int]] = deque(maxlen=n_workers)
    while stack or workers:
        t += 1
        # print(f"{t:4}", " ".join(x[0] if x else "." for x in workers), proc, end=" ")
        done = []
        for key, start in workers:
            if dur[key] + start - t == 0:
                done.append((key, start))
                proc += key
                # print("finished:", key, d[key])
                for nxt in d[key].after:
                    if nxt not in proc and nxt not in stack:
                        insort(stack, nxt)

        for x in done:
            workers.remove(x)
        # print(stack)

        del_stack = []
        for task in stack:

            bef = d[task].before

            is_ready = (
                not bef
                or all(x[0] not in bef for x in workers if x)
                and all(x in proc for x in bef)
            )

            if is_ready and len(workers) != n_workers:
                # print("initiating:", task, d[task])
                workers.append((task, t))
                del_stack.append(task)

        for v in del_stack:
            stack.remove(v)

    # unprocessed letters
    # print("".join(x for x in d.keys() if x not in proc)
    return proc, t


def build_instructions(data: List[Tuple[str, str]]) -> Dict[str, Node]:
    d: Dict[str, Node] = defaultdict(Node)
    for prev, curr in data:
        d[curr].before.add(prev)
        d[prev].after.add(curr)
    return d


def main() -> None:

    ir = r"^Step (\w).+(\w) can begin.$"
    with open("input_data/day_7") as f:
        instructions = build_instructions(re.findall(ir, f.read(), re.M))

    dur1 = {c: 1 for c in string.ascii_uppercase}
    print(*do(instructions, dur1))
    print(T(lambda: do(instructions, dur1)).timeit(500) * 2, "ms per loop")

    dur5 = {c: ord(c) - 4 for c in string.ascii_uppercase}
    print(*do(instructions, dur5, 5))
    print(T(lambda: do(instructions, dur5, 5)).timeit(500) * 2, "ms per loop")


if __name__ == "__main__":
    main()
