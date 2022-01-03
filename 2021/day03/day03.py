"""
Problem 3 of the Advent-of-Code 2021
"""

from typing import Any, List, Set
from collections import Counter


def read_inputs(filename: str) -> List[Any]:
    lines = []
    with open(filename, "r") as fp:
        for line in fp:
            lines.append(line.strip())
    return lines


def part_a(lines: List[str]):
    most_common_string = "".join(Counter(line[i] for line in lines).most_common()[0][0] for i in range(len(lines[0])))
    least_common_string = "".join(Counter(line[i] for line in lines).most_common()[-1][0] for i in range(len(lines[0])))
    return int(most_common_string, 2) * int(least_common_string, 2)


def part_b(lines: List[str]):
    most_popular_lines = set(i for i in lines)
    least_popular_lines = set(i for i in lines)

    for i in range(len(lines[0])):
        most_popular_element = get_most_popular_element(most_popular_lines, i)
        least_popular_element = get_least_popular_element(least_popular_lines, i)

        most_popular_lines = set(x for x in most_popular_lines if x[i] == most_popular_element)
        least_popular_lines = set(x for x in least_popular_lines if x[i] == least_popular_element)

    (a,) = least_popular_lines
    (b,) = most_popular_lines

    return int(a, 2) * int(b, 2)


def get_most_popular_element(inputs: Set[str], index: int):
    counts = Counter(x[index] for x in inputs).most_common()
    if len(counts) == 1:
        return counts[0][0]
    if counts[0][1] == counts[1][1]:
        return "1"
    return counts[0][0]


def get_least_popular_element(inputs: Set[str], index: int):
    counts = Counter(x[index] for x in inputs).most_common()
    if len(counts) == 1:
        return counts[0][0]
    if counts[0][1] == counts[1][1]:
        return "0"
    return counts[-1][0]


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    print(f"Part A: {part_a(inputs)}")
    print(f"Part B: {part_b(inputs)}")
