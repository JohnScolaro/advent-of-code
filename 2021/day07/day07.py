"""
Problem 7 of the Advent-of-Code 2019
"""

import itertools
from typing import Any, List, Set, Tuple
from collections import defaultdict


def read_inputs(filename: str) -> List[Any]:
    with open(filename, "r") as fp:
        for line in fp:
            return [int(x) for x in line.split(",")]


def min_fuel(inputs):
    min_pos = min(inputs)
    max_pos = max(inputs)
    d = {i: 0 for i in range(min_pos, max_pos + 1)}
    for crab in inputs:
        for i in range(min_pos, max_pos + 1):
            d[i] += abs(i - crab)
    return min(d.values())


def min_fuel_b(inputs):
    min_pos = min(inputs)
    max_pos = max(inputs)
    d = {i: 0 for i in range(min_pos, max_pos + 1)}
    for crab in inputs:
        for i in range(min_pos, max_pos + 1):
            d[i] += sum(range(1, abs(i - crab) + 1))
    return min(d.values())


def part_a(inputs) -> int:
    return min_fuel(inputs)


def part_b(inputs) -> int:
    return min_fuel_b(inputs)


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    print(inputs)
    print(f"Part A: {part_a(inputs)}")
    print(f"Part B: {part_b(inputs)}")
