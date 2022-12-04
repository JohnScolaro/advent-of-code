"""
Problem 4 of the Advent-of-Code 2022
"""

from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, "r") as fp:
        for line in fp:
            a, b = line.strip().split(',')
            c, d = (int(x) for x in a.split('-'))
            e, f = (int(x) for x in b.split('-'))
            input_list.append(((c, d), (e, f)))
    return input_list

def contains(a: tuple[int, int], b: tuple[int, int]) -> bool:
    c, d = a
    e, f = b
    return (e >= c and f <= d) or (c >= e and d <= f)

def overlap_at_all(a: tuple[int, int], b: tuple[int, int]) -> bool:
    c, d = a
    e, f = b

    return not ((d < e) or (c > f))

def part_a(input_list: List[int]) -> int:
    return sum(1 if contains(a, b) else 0 for a, b in input_list)



def part_b(input_list: List[int]) -> int:
    return sum(1 if overlap_at_all(a, b) else 0 for a, b in input_list)


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
