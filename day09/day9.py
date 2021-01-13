'''
Solutions for the Advent of Code - Day 9
'''

def get_list_of_numbers(file_path: str) -> list:
    l = []
    with open(file_path, 'r') as fb:
        for line in fb:
            l.append(int(line[:-1]))
    return l

def part_a(list_of_numbers: list, n_previous_numbers: int) -> int:
    i = n_previous_numbers
    while i < len(list_of_numbers):
        if sum_exists_in_list(list_of_numbers, n_previous_numbers, i):
            return list_of_numbers[i]
        i += 1
    return 0

def sum_exists_in_list(list_of_numbers, n, i):
    """
    Returns true if two numbers in the list of numbers can sum together to
    make the number pointed to by index i in the list of numbers.
    """
    sublist = list_of_numbers[i-n:i]
    for x in sublist:
        if list_of_numbers[i] - x in sublist:
            if list_of_numbers[i] / 2 != x:
                return False
    return True

def part_b(list_of_numbers: list, goal: int) -> int:
    """
    Loops over all windows sizes until a successful contigous sum is found.
    """
    i = 2
    while True:
        successful_list = contiguous_sum_of_window(list_of_numbers, i, goal)
        if (successful_list != []):
            return min(successful_list) + max(successful_list)
        else:
            i += 1


def contiguous_sum_of_window(list_of_numbers: list, window_size: int, goal: int) -> list:
    """
    Checks to see if a contiguous window of size window_size can be summed
    together to create the goal number.

    Slides the windows across the whole list.
    """
    sub_list = list_of_numbers[0:window_size]
    i = window_size
    while (i < len(list_of_numbers)):
        if sum(sub_list) == goal:
            return sub_list
        sub_list.pop(0)
        sub_list.append(list_of_numbers[i])
        i += 1
    return []


if __name__ == "__main__":
    list_of_numbers = get_list_of_numbers('input.txt')

    # Part A
    print("Part A: " + str(part_a(list_of_numbers, 25)))

    # Part B
    print("Part B: " + str(part_b(list_of_numbers, part_a(list_of_numbers, 25))))
    