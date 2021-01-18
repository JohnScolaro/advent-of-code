'''
Solutions for the Advent of Code - Day 13
'''

import numpy as np

def get_schedules(input_file: str) -> tuple:
    """ Read the input file into reasonable types. """
    with open('input.txt', 'r') as fb:
        earliest_time = int(fb.readline())
        bus_list = fb.readline().split(',')
        bus_list[-1] = bus_list[-1][:-1]
    return (earliest_time, bus_list)

def get_only_numbers(input_list: list) -> list:
    """ Since part A doesn't use the 'x's, this function removes them."""
    l = []
    for x in input_list:
        try:
            a = int(x)
            l.append(a)
        except:
            pass
    return l

def part_a(start_number: int, schedule: list) -> int:
    """
    Starting at the start time, just iterate through each time and check to
    see if any of the busses have come. When you find one, return the proper
    answer to the question.
    """
    i = start_number
    while True:
        for bus_id in schedule:
            if i % bus_id == 0:
                return (i - start_number) * bus_id
        i += 1

def part_b(schedules: list) -> int:
    """
    Algorithm for calculating the times all the busses depart at the correct
    time for part B.
    """

    # Set starting variables
    multiplier = 1 # Number which we add to the lowest time. Grows.
    lowest_time = 1 # The times we are checking
    max_i = len(schedules) - 1 # Simply tells us when to break
    for i in range(len(schedules)):

        # Skip x's
        if schedules[i] == 'x':
            continue

        delay = i
        bus_id = int(schedules[i])

        # While this bus doesn't arrive at the correct time, keep adding
        # multiplier to the lowest time. It will eventually.
        while (lowest_time + delay) % bus_id != 0:
            lowest_time += multiplier

        # If we are at the end of the list, break.
        if i == max_i:
            break

        # Once we find a time that does sync up, make multiplier the lowest
        # common multiple of the multiplier and the bus ID. The time at which
        # all previous numbers and the current number sync up again will be
        # every multiplier from now on, so no use checking any other numbers.
        multiplier = np.lcm(multiplier, bus_id)

    return lowest_time

if __name__ == "__main__":
    earliest_time, bus_list = get_schedules('input.txt')
    valid_times = get_only_numbers(bus_list)
    print("Part A: " + str(part_a(earliest_time, valid_times)))
    print("Part B: " + str(part_b(bus_list)))
