"""
Problem 1 of the Advent-of-Code 2018

I am doing this for time comparison reasons.
"""

from typing import List, Set


def read_inputs(filename: str) -> List[int]:
    """ Read input file into a list of ints """
    input = []
    with open(filename, 'r') as fp:
        for line in fp:
            input.append(int(line.strip()))
    return input


def part_a(input: List[int]) -> int:
    """ Returns the answer to part A """
    return sum(input)


def part_b(input: List[int]) -> int:
    """ Returns the answer to part B """
    current_value = 0
    history: Set[int] = set()
    while True:
        for i in input:
            current_value += i
            if current_value in history:
                return current_value
            history.add(current_value)


if __name__ == "__main__":
    input = read_inputs('input.txt')
    print("Part A: {}".format(part_a(input)))
    print("Part B: {}".format(part_b(input)))
