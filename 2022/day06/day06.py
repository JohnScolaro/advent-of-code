"""
Problem 5 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools
from collections import Counter


def read_inputs(filename: str) -> List[Any]:
    input_text = []
    with open(filename, "r") as fp:
        for line in fp:
            input_text.append(line.strip())
    return input_text


def part_a(input_list: List[int]) -> int:
    a = 0
    for i, j, k, l in more_itertools.windowed(input_list[0], 4):
        if len(set([i, j, k, l])) == 4:
            return a + 4
        else:
            a += 1


def part_b(input_list: List[int]) -> int:
    xx = 0
    for a, b, c, d, e, f, g, h, i, j, k, l, m, n in more_itertools.windowed(input_list[0], 14):
        if len(set([a, b, c, d, e, f, g, h, i, j, k, l, m, n])) == 14:
            return xx + 14
        else:
            xx += 1


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
