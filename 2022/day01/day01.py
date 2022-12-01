"""
Problem 1 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools


def read_inputs(filename: str) -> List[Any]:
    elves = [[]]
    with open(filename, "r") as fp:
        for line in fp:
            if line.strip() != "":
                elves[-1].append(int(line.strip()))
            else:
                elves.append([])
    return elves


def part_a(input_list: List[int]) -> int:
    return max(sum(elf) for elf in input_list)


def part_b(input_list: List[int]) -> int:
    a = list(sum(elf) for elf in input_list)
    a.sort()
    return sum([a[-1], a[-2], a[-3]])


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
