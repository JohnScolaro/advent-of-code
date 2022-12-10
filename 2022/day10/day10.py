"""
Problem 10 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools

INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]

def read_inputs(filename: str) -> List[Any]:
    input_list = []
    with open(filename, "r") as fp:
        for line in fp:
            input_list.append(line.strip())
    return input_list


def part_a(input_list: List[int]) -> int:
    cycle = 1
    register = 1
    times_to_add_different_things = {}
    input_index = 0
    seconds_remaining_on_current_instruction=0
    signals = []
    while cycle <= 220:

        # during cycle
        if seconds_remaining_on_current_instruction == 0:
            line = input_list[input_index]
            if line == 'noop':
                input_index += 1
            else:
                num_to_add = int(line.split()[1])
                times_to_add_different_things[cycle + 2] = times_to_add_different_things.get(cycle + 1, 0) + num_to_add
                seconds_remaining_on_current_instruction = 1
                input_index += 1
        else:
            seconds_remaining_on_current_instruction -= 1

        # after cycle
        cycle += 1
        if cycle in times_to_add_different_things:
            register += times_to_add_different_things.pop(cycle)

        # readouts
        if cycle in INTERESTING_CYCLES:
            signals.append(cycle * register)

    return sum(signals)

def part_b(input_list: List[int]) -> int:
    cycle = 1
    register = 1
    times_to_add_different_things = {}
    input_index = 0
    seconds_remaining_on_current_instruction=0
    signals = []
    while cycle <= 240:

        # during cycle
        if seconds_remaining_on_current_instruction == 0:
            line = input_list[input_index]
            if line == 'noop':
                input_index += 1
            else:
                num_to_add = int(line.split()[1])
                times_to_add_different_things[cycle + 2] = times_to_add_different_things.get(cycle + 1, 0) + num_to_add
                seconds_remaining_on_current_instruction = 1
                input_index += 1
        else:
            seconds_remaining_on_current_instruction -= 1

        print('#' if abs(register - (cycle%40)+1) <= 1 else '.', end='')
        if cycle%40 == 0:
            print("\n", end='')

        # after cycle
        cycle += 1
        if cycle in times_to_add_different_things:
            register += times_to_add_different_things.pop(cycle)



if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    part_b(input_list)
