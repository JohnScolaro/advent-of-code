"""
Problem 8 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools
from collections import Counter


def read_inputs(filename: str) -> List[Any]:
    lines = []
    with open(filename, "r") as fp:
        for line in fp:
            row = []
            for char in line.strip():
                row.append(int(char))
            lines.append(row.copy())

    return lines


def part_a(input_list: List[int]) -> int:
    visible_num = 0
    for y in range(len(input_list)):
        for x in range(len(input_list[0])):
            options = get_all_options(input_list, x, y)
            if any(input_list[y][x] > max(option) for option in get_all_options(input_list, x, y)):
                visible_num += 1

    return visible_num


def get_all_options(input_list, x, y):
    left_set = set()
    right_set = set()
    up_set = set()
    down_set = set()

    x1 = x - 1
    while x1 != -1:
        left_set.add(input_list[y][x1])
        x1 -= 1

    x2 = x + 1
    while x2 != len(input_list[y]):
        right_set.add(input_list[y][x2])
        x2 += 1

    y1 = y - 1
    while y1 != -1:
        up_set.add(input_list[y1][x])
        y1 -= 1

    y2 = y + 1
    while y2 != len(input_list[y]):
        down_set.add(input_list[y2][x])
        y2 += 1

    if len(left_set) == 0:
        left_set = {-1}
    if len(right_set) == 0:
        right_set = {-1}
    if len(up_set) == 0:
        up_set = {-1}
    if len(down_set) == 0:
        down_set = {-1}

    return [left_set, right_set, up_set, down_set]


def part_b(input_list: List[int]) -> int:
    scores = []
    for y in range(len(input_list)):
        for x in range(len(input_list[0])):
            scores.append(get_score(input_list, x, y))

    print(scores)
    return max(scores)


def get_score(input_list, x, y):
    l = 0
    r = 0
    u = 0
    d = 0

    x1 = x - 1
    while x1 != -1:
        if input_list[y][x1] >= input_list[y][x]:
            l += 1
            break
        else:
            x1 -= 1
            l += 1

    x2 = x + 1
    while x2 < len(input_list[y]):
        if input_list[y][x2] >= input_list[y][x]:
            r += 1
            break
        else:
            x2 += 1
            r += 1

    y1 = y - 1
    while y1 != -1:
        if input_list[y1][x] >= input_list[y][x]:
            u += 1
            break
        else:
            y1 -= 1
            u += 1

    y2 = y + 1
    while y2 != len(input_list):
        if input_list[y2][x] >= input_list[y][x]:
            d += 1
            break
        else:
            y2 += 1
            d += 1

    return l * r * u * d


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
