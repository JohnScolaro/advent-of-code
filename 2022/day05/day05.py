"""
Problem 5 of the Advent-of-Code 2022
"""

from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, "r") as fp:
        for line in fp:
            input_list.append(line.strip())
    return input_list


def part_a(input_list: List[int]) -> int:
    return input_list


def part_b(input_list: List[int]) -> int:
    return input_list


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    # print(f"Part B: {part_b(input_list)}")
