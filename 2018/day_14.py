#!/usr/bin/env python3.7
"""--- Day 14: Chocolate Charts ---"""


def main():
    elf1, elf2 = 0, 1
    values = ["51589", "01245", "92510", "59414", "505961"]
    find = list(map(int, values[3]))
    mlf = -5
    recipes = [3, 7]
    n_rec = 2
    while find != recipes[mlf:]:
        elf1 = (elf1 + recipes[elf1] + 1) % n_rec
        elf2 = (elf2 + recipes[elf2] + 1) % n_rec

        s = recipes[elf1] + recipes[elf2]
        if s > 9:
            recipes.append(s // 10)
            n_rec += 1

        recipes.append(s % 10)
        n_rec += 1

    print("".join(map(str, recipes[mlf:])), elf1, elf2)
    print(len(recipes) + mlf)


if __name__ == "__main__":
    main()
