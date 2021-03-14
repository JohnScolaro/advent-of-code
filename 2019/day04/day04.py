"""
Problem 4 of the Advent-of-Code 2019
"""

from collections import Counter

def read_inputs(filename: str) -> tuple:
    """
    Reads the input file which will contain a single line: 'xxxxxx-xxxxxx'
    where x's are actually numbers. This function returns a tuple with the two
    numbers in it.
    """
    l = []
    with open(filename, 'r') as fp:
        for line in fp:
            l.append(line.strip())
    min = int(l[0].split('-')[0])
    max = int(l[0].split('-')[1])
    return (min, max)

def generate_possible_numbers(min: int, max: int) -> set:
    """
    Returns a set of all possible numbers between but not including the two
    initial max and min numbers.
    """
    return set(range(min + 1, max))

def remove_numbers_without_duplicates(possible_numbers: set) -> None:
    """
    Takes a set of numbers, modifies that set inline to remove all numbers that
    don't have at least a single duplicate.
    """
    numbers_to_remove = set()
    for possible_number in possible_numbers:
        str_num = str(possible_number)
        duplicate = False
        for i in range(len(str_num) - 1):
            if str_num[i] == str_num[i+1]:
                duplicate = True
        if not duplicate:
            numbers_to_remove.add(possible_number)
    for number_to_remove in numbers_to_remove:
        possible_numbers.remove(number_to_remove)

def remove_non_increasing_numbers(possible_numbers: set) -> None:
    """
    Takes a set of numbers and modifies that set inline to remove any numbers
    that contains consecutive digits that decrease. Increasing and staying the
    same are both acceptable. 
    """
    numbers_to_remove = set()
    for possible_number in possible_numbers:
        num_list = [int(x) for x in list(str(possible_number))]
        for i in range(len(num_list) - 1):
            if num_list[i] > num_list[i+1]:
                numbers_to_remove.add(possible_number)
    for number_to_remove in numbers_to_remove:
        possible_numbers.remove(number_to_remove)

def remove_non_twin_numbers(possible_numbers: set) -> None:
    """
    Takes a set of numbers and modifies that set inline to remove numbers
    without an 'twins' in it. Twins are when there are ONLY 2 consecutive
    duplicate numbers.

    123345 -> Not removed
    123335 -> Removed
    112222 -> Not removed
    """
    numbers_to_remove = set()
    for possible_number in possible_numbers:
        c = Counter(list(str(possible_number)))
        if 2 not in c.values():
            numbers_to_remove.add(possible_number)
    for number_to_remove in numbers_to_remove:
        possible_numbers.remove(number_to_remove)

def part_a(filename: str) -> set:
    """
    For part A of this challenge we are finding the total number of possible
    passwords which satisfy the conditions. This function return a set of all
    the possible satisfying conditions.
    """
    min, max = read_inputs(filename)
    possible_numbers = generate_possible_numbers(min, max)
    remove_numbers_without_duplicates(possible_numbers)
    remove_non_increasing_numbers(possible_numbers)
    return possible_numbers

def part_b(filename: str) -> set:
    """
    Part B builds on part A by additionally not letting us use combinations
    with more than 2 consecutive identical digits.
    """
    possible_numbers = part_a(filename)
    remove_non_twin_numbers(possible_numbers)
    return possible_numbers


if __name__ == "__main__":
    print("Part A: " + str(len(part_a('input.txt'))))
    print("Part B: " + str(len(part_b('input.txt'))))
    