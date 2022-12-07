"""
Problem 7 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools


def read_inputs(filename: str) -> List[Any]:
    input_lines = []
    with open(filename, "r") as fp:
        for line in fp:
            input_lines.append(line.strip())
    return input_lines


def part_a(input_lines: List[int]) -> int:
    structure = {"/": {}}
    path = []

    for line in input_lines:
        split_line = line.split()
        if split_line[0] == "$":

            # cd
            if split_line[1] == "cd":
                if split_line[2] == "..":
                    path.pop(-1)
                else:
                    path.append(split_line[2])
            # ls
            elif split_line[1] == "ls":
                pass
            else:
                raise Exception("Shouldnt get here")
        else:
            if split_line[0] == "dir":
                add_dir(structure, path, split_line[1])
            else:
                add_file(structure, path, split_line[1], int(split_line[0]))

    a = []
    get_all_dir_sizes(a, structure)
    # return sum(b for b in a if b < 100000)

    current_space = 70_000_000 - max(a)
    required_space = 30_000_000
    difference = required_space - current_space
    # find smallest number larger than difference
    return min([x for x in a if x >= difference])

    return a


def add_file(structure, path, file_name, size):
    a = structure
    for x in path:
        a = a[x]
    a[file_name] = size


def add_dir(structure, path, dir_name):
    a = structure
    for x in path:
        a = a[x]
    a[dir_name] = {}


def part_b(input_lines: List[int]) -> int:
    return input_lines


def get_dir_size(structure):
    total = 0
    for k, v in structure.items():
        if isinstance(v, dict):
            total += get_dir_size(v)
        else:
            total += v

    return total


def get_all_dir_sizes(all_sizes: list, structure):
    for k, v in structure.items():
        if isinstance(v, dict):
            all_sizes.append(get_dir_size(v))
            get_all_dir_sizes(all_sizes, v)


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    # print(f"Part B: {part_b(input_list)}")
