"""
Problem 6 of the Advent-of-Code 2019
"""

import itertools
from typing import Any, Dict, List, Set, Tuple
from collections import defaultdict


def read_inputs(filename: str) -> List[Any]:
    with open(filename, "r") as fp:
        for line in fp:
            list_of_ages = [int(x) for x in line.split(",")]
    dict_of_ages = defaultdict(int)
    for age in list_of_ages:
        dict_of_ages[age] += 1
    return dict(dict_of_ages)


def simulate_one_day(fish_ages: Dict[int, int]) -> Dict[int, int]:
    new_fish_ages = {}
    for i in range(0, 8):
        new_fish_ages[i] = fish_ages.get(i + 1, 0)
    new_fish_ages[6] += fish_ages.get(0, 0)
    new_fish_ages[8] = fish_ages.get(0, 0)
    return new_fish_ages


def part_a(dict_of_ages: Dict[int, int]) -> int:
    fish_ages = dict_of_ages.copy()
    for _ in range(80):
        fish_ages = simulate_one_day(fish_ages)
    return sum(v for v in fish_ages.values())


def part_b(dict_of_ages: Dict[int, int]) -> int:
    fish_ages = dict_of_ages.copy()
    for _ in range(256):
        fish_ages = simulate_one_day(fish_ages)
    return sum(v for v in fish_ages.values())


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    print(f"Part A: {part_a(inputs)}")
    print(f"Part B: {part_b(inputs)}")
