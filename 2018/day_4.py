#!/usr/bin/env python3.7
"""--- Day 4: Repose Record ---"""

from typing import List, Dict, Optional, Any, Tuple, Callable
import re
import bisect
from collections import defaultdict, namedtuple

Sleep = namedtuple("Sleep", "start month day end")


class SleepCounter(defaultdict):
    def __init__(self, g: "Guard") -> None:
        super().__init__(int)
        for s in g.sleeps:
            for i in range(int(s.start), int(s.end)):
                self[i] += 1

    def __repr__(self) -> str:
        return "".join("#" if self[i] else "." for i in range(60))


class Guard:
    __slots__ = ("sleeps", "id", "tot")

    def __init__(self, _id: str) -> None:
        self.sleeps: List[Sleep] = []
        self.id = int(_id[1:])
        self.tot = 0

    def __repr__(self) -> str:
        return f"<Guard #{self.id} x{len(self.sleeps)}:{self.tot}m>"

    def sleep(self, start: str, log_entry: str) -> None:
        s = Sleep(start, log_entry[1], log_entry[2], log_entry[4])
        self.sleeps.append(s)
        self.tot += int(s.end) - int(s.start)

    @property
    def max_minute(self) -> Tuple[int, int]:
        items = SleepCounter(self).items() or [(0, 0)]
        return max(items, key=lambda x: x[1])


class GuardsDict(Dict[str, Guard]):
    def __init__(self, logs: List[str]) -> None:
        curr_id = start = ""
        for log in logs:
            action = log[5]
            if action == "falls asleep":
                start = log[4]
            elif action == "wakes up":
                self[curr_id].sleep(start, log)
            else:
                curr_id = action.split()[1]  # Guard $ID begins shift

    def __missing__(self, key: str) -> Guard:
        self[key] = Guard(key)
        return self[key]

    def filter_max(self, desc: str, func: Callable[[Guard], int]) -> None:
        top = max(self.values(), key=func)
        print(desc, "guard:", top)
        max_min, max_min_count = top.max_minute
        print(f"    asleep @ 00:{max_min} {max_min_count} times -", max_min * top.id)


def main() -> None:
    with open("input_data/day_4") as f:
        data = f.read()

    sleep_re = r"^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)$"
    guards = GuardsDict(sorted(re.findall(sleep_re, data, re.M)))

    # guard with largest total minutes slept
    guards.filter_max("sleepiest", lambda g: g.tot)
    # print()
    # guard who falls asleep at a given minute the most
    guards.filter_max("consistent", lambda g: g.max_minute[1])


if __name__ == "__main__":
    main()
