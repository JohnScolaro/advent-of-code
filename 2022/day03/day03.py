"""
Problem 3 of the Advent-of-Code 2022
"""

from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, "r") as fp:
        for line in fp:
            input_list.append(line.strip())
    return input_list


def part_a(input_list: List[int]) -> int:
    errors = []
    for rucksack in input_list:
        first_half = rucksack[:int(len(rucksack)/2)]
        second_half = rucksack[int(len(rucksack)/2):]
        common_element = set(first_half).intersection(set(second_half))
        errors.append(next(iter(common_element)))

    return sum(ord(error) - 96 if error.islower() else ord(error) - 38 for error in errors)


def part_b(input_list: List[int]) -> int:
    common_items = []
    elf_thruples = list(zip(input_list[0::3], input_list[1::3], input_list[2::3]))
    for a, b, c in elf_thruples:
        common_items.append(next(iter(set(a).intersection(set(b), set(c)))))
    return sum(ord(common_item) - 96 if common_item.islower() else ord(common_item) - 38 for common_item in common_items)


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
