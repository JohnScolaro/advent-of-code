"""
Solutions for the Advent of Code - Day 10
"""

import bisect


def get_sorted_input(file_name: str) -> list:
    """ Turn the input file into a sorted list """
    s = []
    with open(file_name, 'r') as fb:
        for line in fb:
            bisect.insort_left(s, int(line[:-1]))
    return s


def part_a(adapter_list: list) -> int:
    """ Return number of 1 jolt differences * number of 3 jolt differences """
    one_jolt_differences = 1
    three_jolt_differences = 1
    i = 0
    while i < len(adapter_list) - 1:
        jolt_difference = adapter_list[i+1] - adapter_list[i]
        if jolt_difference == 1:
            one_jolt_differences += 1
        if jolt_difference == 3:
            three_jolt_differences += 1
        i += 1

    return one_jolt_differences * three_jolt_differences


def part_b(adapter_list: list) -> int:
    """
    Return the total number of combinations in which you can use your adapters.
    """
    # Add 0 in to represent the wall socket
    bisect.insort_left(adapter_list, 0)

    # Break list into sub lists.
    # A sublist is part of the list where numbers are closer than 3 together.
    all_sub_lists = []
    sub_list_builder = []
    for i in range(len(adapter_list)):
        sub_list_builder.append(adapter_list[i])
        if i == len(adapter_list) - 1:
            break
        if adapter_list[i+1] - adapter_list[i] == 3:
            all_sub_lists.append(sub_list_builder)
            sub_list_builder = []
    all_sub_lists.append(sub_list_builder)

    # Calculate the number of permutations for sublists.
    for i in range(len(all_sub_lists)):
        all_sub_lists[i] = find_perms_in_list(all_sub_lists[i])

    # Multiple sublist permutations together for get permutations for entire set of adapters.
    prod = 1
    for x in all_sub_lists:
        prod *= x

    return prod


def find_perms_in_list(adapter_list: list) -> int:
    """
    Recursively find the number of possible permutations :)
    """
    if len(adapter_list) <= 2:
        return 1
    if len(adapter_list) == 3:
        return 2
    return find_perms_in_list(adapter_list[1:]) + \
        find_perms_in_list(adapter_list[2:]) + \
        find_perms_in_list(adapter_list[3:])


if __name__ == "__main__":
    s = get_sorted_input('input.txt')
    print("Part A: " + str(part_a(s)))
    print("Part B: " + str(part_b(s)))
