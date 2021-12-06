"""
Problem 1 of the Advent-of-Code 2019
"""

import itertools
from typing import Any, List, Set, Tuple
from collections import defaultdict


def read_inputs(filename: str) -> List[Any]:
    inputs = []
    with open(filename, "r") as fp:
        for line in fp:
            start_coords = line.split("->")[0].strip()
            end_coords = line.split("->")[1].strip()
            start_coords = (int(start_coords.split(",")[0]), int(start_coords.split(",")[1]))
            end_coords = (int(end_coords.split(",")[0]), int(end_coords.split(",")[1]))
            inputs.append((start_coords, end_coords))
    return inputs


Coord = Tuple[Tuple[int, int], Tuple[int, int]]


def are_coords_horizontal_or_vertical(coord: Coord) -> bool:
    return coord[0][0] == coord[1][0] or coord[0][1] == coord[1][1]


def are_coords_diagonal(coord: Coord) -> bool:
    return abs(coord[0][0] - coord[1][0]) == abs(coord[0][1] - coord[1][1])


def get_points_between_coords(coord: Coord) -> Set[Tuple[int, int]]:
    if coord[0][0] == coord[1][0]:
        x_iterable = itertools.cycle([coord[0][0]])
    else:
        x_iterable = range(coord[0][0], coord[1][0], 1 if coord[0][0] < coord[1][0] else -1)

    if coord[0][1] == coord[1][1]:
        y_iterable = itertools.cycle([coord[1][1]])
    else:
        y_iterable = range(coord[0][1], coord[1][1], 1 if coord[0][1] < coord[1][1] else -1)

    return set((x, y) for x, y in zip(x_iterable, y_iterable)).union(set([coord[1]]))


def part_a(inputs: List[str]) -> int:
    d = defaultdict(int)
    for coord in inputs:
        if are_coords_horizontal_or_vertical(coord):
            for point in get_points_between_coords(coord):
                d[point] += 1
    return len([x for x in d if d[x] >= 2])


def part_b(inputs: List[str]) -> int:
    d = defaultdict(int)
    for coord in inputs:
        if are_coords_horizontal_or_vertical(coord) or are_coords_diagonal(coord):
            for point in get_points_between_coords(coord):
                d[point] += 1
    return len([x for x in d if d[x] >= 2])


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    print(f"Part A: {part_a(inputs)}")
    print(f"Part B: {part_b(inputs)}")
