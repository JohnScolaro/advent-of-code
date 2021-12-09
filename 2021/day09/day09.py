"""
Problem 9 of the Advent-of-Code 2019
"""
from typing import Any, Dict, List, Optional, Set, Tuple
from functools import reduce


def read_inputs(filename: str) -> List[Any]:
    inputs = []
    with open(filename, "r") as fp:
        for line in fp:
            inputs.append([int(x) for x in line.strip()])
    return inputs


def get_point(inputs, x: int, y: int) -> Optional[None]:
    if x < 0 or y < 0 or x >= len(inputs) or y >= len(inputs[0]):
        return None
    return inputs[x][y]


def part_a(inputs) -> int:
    s = 0
    for x in range(len(inputs)):
        for y in range(len(inputs[0])):
            if is_lowest_point(inputs, x, y):
                s += inputs[x][y] + 1
    return s


def is_lowest_point(inputs, x, y) -> bool:
    return inputs[x][y] < min(
        get_point(inputs, x + i, y + j)
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if get_point(inputs, x + i, y + j) is not None
    )


def get_move_to_lower_point(inputs, x, y):
    p = get_point(inputs, x, y)
    for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        p2 = get_point(inputs, x + dx, y + dy)
        if (p2 is not None) and (p2 < p):
            return (dx, dy)


def get_end_point_from_start_point(inputs, x, y) -> Tuple[int, int]:
    if inputs[x][y] == 9:
        return (x, y)
    while not is_lowest_point(inputs, x, y):
        dx, dy = get_move_to_lower_point(inputs, x, y)
        x += dx
        y += dy
    return (x, y)


def part_b(inputs) -> int:
    d = {}
    for i in range(len(inputs)):
        for j in range(len(inputs[0])):
            end_point = get_end_point_from_start_point(inputs, i, j)
            d[end_point] = d.get(end_point, 0) + 1
    return reduce(lambda x, y: x * y, list(sorted(d.values(), reverse=True))[0:3])


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    print(f"Part A: {part_a(inputs)}")
    print(f"Part B: {part_b(inputs)}")
