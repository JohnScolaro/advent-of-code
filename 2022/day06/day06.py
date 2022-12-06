"""
Problem 5 of the Advent-of-Code 2022
"""

import more_itertools


def read_inputs(filename: str) -> str:
    with open(filename, "r") as fp:
        for line in fp:
            return line.strip()


def part_x(input: str, window_length: int) -> int:
    for i, b in enumerate(more_itertools.windowed(input, window_length)):
        if len(set(b)) == window_length:
            return i + window_length


if __name__ == "__main__":
    input = read_inputs("input.txt")
    print(f"Part A: {part_x(input, 4)}")
    print(f"Part B: {part_x(input, 14)}")
