"""
Problem 1 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools
from typing import Any


def read_inputs(filename: str) -> List[Any]:
    input_lines = []
    with open(filename, "r") as fp:
        for line in fp:
            input_lines.append(line.strip())

    processed_lines: tuple[list, list] = []
    for a, b, _ in more_itertools.windowed(input_lines, 3, step=3):
        processed_lines.append((process(a), process(b)))
    return processed_lines


def process(input: str) -> list[Any]:
    try:
        return int(input)
    except:
        #TODO


def part_a(processed_lines: list[Any]) -> Any:
    for a, b in processed_lines:
        print(a)
        print(b)
        print("")

    return processed_lines


# def part_b(input_list: List[int]) -> int:
#     a = list(sum(elf) for elf in input_list)
#     a.sort()
#     return sum([a[-1], a[-2], a[-3]])


if __name__ == "__main__":
    input_list = read_inputs("input2.txt")
    print(f"Part A: {part_a(input_list)}")
    # print(f"Part B: {part_b(input_list)}")
