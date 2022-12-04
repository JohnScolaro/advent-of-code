"""
Problem 2 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools


THEM_MAP = {"A": 1, "B": 2, "C": 3}
ME_MAP = {"X": 1, "Y": 2, "Z": 3}


def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, "r") as fp:
        for line in fp:
            input_list.append((line.strip().split(" ")[0], line.strip().split(" ")[1]))
    return input_list


def part_a(input_list: List[int]) -> int:
    total = 0
    for game in input_list:
        them = THEM_MAP[game[0]]
        me = ME_MAP[game[1]]

        if ((me - 1) - (them - 1)) % 3 == 1:
            total += 6 + me
        elif ((me - 1) - (them - 1)) % 3 == 0:
            total += 3 + me
        elif ((me - 1) - (them - 1)) % 3 == 2:
            total += 0 + me

    return total


def part_b(input_list: List[int]) -> int:
    total = 0
    for game in input_list:
        them = THEM_MAP[game[0]]

        if game[1] == "X":
            me = them - 1
            if me == 0:
                me = 3
        elif game[1] == "Y":
            me = them
        elif game[1] == "Z":
            me = them + 1
            if me == 4:
                me = 1

        if ((me - 1) - (them - 1)) % 3 == 1:
            total += 6 + me
        elif ((me - 1) - (them - 1)) % 3 == 0:
            total += 3 + me
        elif ((me - 1) - (them - 1)) % 3 == 2:
            total += 0 + me

    return total


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
