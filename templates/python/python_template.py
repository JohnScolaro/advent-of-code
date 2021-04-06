"""
Problem 1 of the Advent-of-Code 2019
"""

from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    input = []
    with open(filename, 'r') as fp:
        for line in fp:
            input.append(line.strip())
    return input


if __name__ == "__main__":
    input = read_inputs('input.txt')
    print(input)
