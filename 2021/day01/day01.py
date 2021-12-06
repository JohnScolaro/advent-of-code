"""
Problem 1 of the Advent-of-Code 2019
"""

from typing import Any, List
import more_itertools

def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, 'r') as fp:
        for line in fp:
            input_list.append(int(line.strip()))
    return input_list

def part_a(input_list: List[int]) -> int:
    return sum(1 if x < y else 0 for x, y in more_itertools.windowed(input_list, 2))

def part_b(input_list: List[int]) -> int:
    return sum(1 if sum((i, j, k)) < sum((j, k, l)) else 0 for i, j, k, l in more_itertools.windowed(input_list, 4))

if __name__ == "__main__":
    input_list = read_inputs('input.txt')
    print(f'Part A: {part_a(input_list)}')
    print(f'Part B: {part_b(input_list)}')
