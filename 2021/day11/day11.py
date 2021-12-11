"""
Problem 11 of the Advent-of-Code 2019
"""
from typing import Any, Dict, List, Optional, Set, Tuple
from functools import reduce
import copy

adj = [(1, 1), (1, 0), (1, -1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]


def read_inputs(filename: str) -> List[Any]:
    lines = []
    with open(filename, "r") as fp:
        for line in fp:
            lines.append([int(x) for x in line.strip()])
    return lines


def increase_all_by_one(inputs):
    for r in range(len(inputs)):
        for c in range(len(inputs[r])):
            inputs[r][c] += 1


def handle_explodes(inputs):
    num_explodes = 0
    for r in range(len(inputs)):
        for c in range(len(inputs[r])):
            if inputs[r][c] > 9:
                inputs[r][c] = 0
                num_explodes += 1
                for dx, dy in adj:
                    r2 = r + dx
                    c2 = c + dy
                    if r2 < 0 or r2 >= len(inputs):
                        continue
                    if c2 < 0 or c2 >= len(inputs[0]):
                        continue
                    if inputs[r2][c2] == 0:
                        continue
                    else:
                        inputs[r2][c2] += 1
    return num_explodes


def part_a(lines) -> int:
    explodes = 0
    for i in range(100):
        increase_all_by_one(lines)
        explodes_this_time = 0
        while True:
            new_explodes = handle_explodes(lines)
            if new_explodes == 0:
                break
            explodes_this_time += new_explodes
        explodes += explodes_this_time
    return explodes


def part_b(lines) -> int:
    time_step = 0
    while True:
        increase_all_by_one(lines)
        explodes_this_time = 0
        while True:
            new_explodes = handle_explodes(lines)
            if new_explodes == 0:
                break
            explodes_this_time += new_explodes
        if explodes_this_time == 100:
            return time_step + 1
        else:
            time_step += 1


if __name__ == "__main__":
    lines = read_inputs("input.txt")
    print(f"Part A: {part_a(copy.deepcopy(lines))}")
    print(f"Part B: {part_b(copy.deepcopy(lines))}")
