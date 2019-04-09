#!/usr/bin/env python3.7
"""--- Day 8: Memory Maneuver ---"""
from typing import List, Tuple
from collections import namedtuple

Node = namedtuple("Node", "n_child n_meta child meta")


def node_sum(node: Node) -> int:
    if not node.child:
        return sum(node.meta)
    return sum(node_sum(node.child[i - 1]) for i in node.meta if i <= node.n_child)


def build_tree(data: List[int]) -> Tuple[Node, int]:
    meta_sum = 0
    parents: List[Node] = []
    n = Node(data[0], data[1], [], [])
    i = 2
    while i < len(data):
        if n.n_child == len(n.child):
            n.meta.extend(data[i : i + n.n_meta])
            meta_sum += sum(n.meta)
            i += n.n_meta
            if parents:
                p = parents.pop()
                p.child.append(n)
                n = p
        else:
            parents.append(n)
            n = Node(data[i], data[i + 1], [], [])
            i += 2
    return n, meta_sum


def main() -> None:
    with open("input_data/day_8") as f:
        data = f.read()
    # data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

    root, meta_sum = build_tree(list(map(int, data.split())))
    print(meta_sum)
    print(node_sum(root))


if __name__ == "__main__":
    main()
