"""
Problem 2 of the Advent-of-Code 2019
"""

from typing import Any, List

def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, 'r') as fp:
        for line in fp:
            input_list.append(line.strip())
    return input_list

def part_a(input_list: List[int]) -> int:
    z = 0
    x = 0
    for i in input_list:
        if 'forward' in i:
            x += int(i.split()[-1])
        if 'up' in i:
            z -= int(i.split()[-1])
        if 'down' in i:
            z += int(i.split()[-1])

    return x * z

def part_b(input_list: List[int]) -> int:
    aim = 0
    z = 0
    x = 0
    for i in input_list:
        if 'forward' in i:
            x += int(i.split()[-1])
            z += (int(i.split()[-1]) * aim)
        if 'up' in i:
            aim -= int(i.split()[-1])
        if 'down' in i:
            aim += int(i.split()[-1])

    return x * z

if __name__ == "__main__":
    input_list = read_inputs('input.txt')
    print(f'Part A: {part_a(input_list)}')
    print(f'Part B: {part_b(input_list)}')
