"""
Problem 13 of the Advent-of-Code 2019
"""
from typing import Any, Dict, List, Optional, Set, Tuple
import copy


def read_inputs(filename: str) -> List[Any]:
    coords = set()
    instructions = []
    with open(filename, "r") as fp:
        for line in fp:
            if "," in line:
                coords.add(tuple([int(x) for x in line.strip().split(",")]))
            elif "=" in line:
                axis = line.strip().split(" ")[-1].split("=")[0]
                position_of_fold = int(line.strip().split(" ")[-1].split("=")[-1])
                instructions.append((axis, position_of_fold))

    return coords, instructions


def fold(coords: Set[Tuple[int, int]], axis: str, position: int) -> Set[Tuple[int, int]]:
    if axis == "x":
        new_coords = set([(x - (2 * (x - position)), y) if x > position else (x, y) for x, y in coords])
    else:
        new_coords = set([(x, y - (2 * (y - position))) if y > position else (x, y) for x, y in coords])
    return new_coords


def part_a(coords, instructions) -> int:
    return len(fold(coords, instructions[0][0], instructions[0][1]))


def part_b(coords, instructions) -> int:
    for instruction in instructions:
        coords = fold(coords, instruction[0], instruction[1])

    print("Part B:")
    for x in range(7):
        for y in range(40):
            if (y, x) in coords:
                print("#", end="")
            else:
                print(" ", end="")
        print("")
    return coords


if __name__ == "__main__":
    coords, instructions = read_inputs("input.txt")
    print(f"Part A: {part_a(coords, instructions)}")
    print(part_b(coords, instructions))
