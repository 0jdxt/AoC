#!/usr/bin/env python3.7
"""--- Day 16: Chronal Classification ---"""
import re
from typing import Dict, Callable, List, Set
from collections import defaultdict
from pprint import pprint


registers = [0] * 4


def addr(A, B, C):
    registers[C] = registers[A] + registers[B]


def addi(A, B, C):
    registers[C] = registers[A] + B


def mulr(A, B, C):
    registers[C] = registers[A] * registers[B]


def muli(A, B, C):
    registers[C] = registers[A] * B


def banr(A, B, C):
    registers[C] = registers[A] & registers[B]


def bani(A, B, C):
    registers[C] = registers[A] & B


def borr(A, B, C):
    registers[C] = registers[A] | registers[B]


def bori(A, B, C):
    registers[C] = registers[A] | B


def setr(A, B, C):
    registers[C] = registers[A]


def seti(A, B, C):
    registers[C] = A


def gtir(A, B, C):
    registers[C] = int(A > registers[B])


def gtri(A, B, C):
    registers[C] = int(registers[A] > B)


def gtrr(A, B, C):
    registers[C] = int(registers[A] > registers[B])


def eqir(A, B, C):
    registers[C] = int(A == registers[B])


def eqri(A, B, C):
    registers[C] = int(registers[A] == B)


def eqrr(A, B, C):
    registers[C] = int(registers[A] == registers[B])


ops = set(
    [
        addi,
        addr,
        muli,
        mulr,
        bani,
        banr,
        borr,
        bori,
        setr,
        seti,
        eqir,
        eqri,
        eqrr,
        gtir,
        gtri,
        gtrr,
    ]
)


print = pprint

if __name__ == "__main__":
    with open("input_data/day_16") as f:
        data = f.read().split("\n\n\n")

    n_gt2 = 0
    poss_map: List = [set() for _ in range(len(ops))]
    sample_re = r"Before: \[(.+)\]\n(.+)\nAfter:  \[(.+)\]"

    for b, i, a in re.findall(sample_re, data[0]):
        after = list(map(int, a.split(", ")))
        before = list(map(int, b.split(", ")))
        ins = i.split()
        curr_poss = poss_map[int(ins[0])]
        instruction = tuple(map(int, ins[1:]))

        n_ops = 0
        for op in ops:
            if op in curr_poss:
                n_ops += 1
            else:
                registers = before.copy()
                op(*instruction)
                if registers == after:
                    curr_poss.add(op)
                    n_ops += 1

        if n_ops > 2:
            n_gt2 += 1

    print(n_gt2)

    opcodes: Dict[int, Callable] = {}
    single = True
    taken: Set = set()
    while single:
        single = False
        for oc, fns in enumerate(poss_map):
            fns -= taken
            if len(fns) == 1:
                fn = fns.pop()
                opcodes[oc] = fn
                taken.add(fn)
                single = True

    print(opcodes)

    registers = [0] * 4
    inst_re = r"^(\d+) (.+)$"
    for oc, args in re.findall(inst_re, data[1], re.M):
        opcodes[int(oc)](*map(int, args.split()))

    print(registers)
