"""
Problem 3 of the Advent-of-Code 2019
"""

from collections import defaultdict
from typing import List


def read_inputs(filename: str) -> List[str]:
    """
    Reads from filename a list of strings. The list has only two lines though,
    the first and second line of the input file. Further splitting on ','s is
    done later.
    """
    input = []
    with open(filename, 'r') as fp:
        for line in fp:
            input.append(line.strip())
    return input


def get_instructions_from_string(string_of_instructions: str) -> list:
    """
    Returns a list of tuples like so: ('U', 3)
    """
    return [(x[0], int(x[1:])) for x in string_of_instructions.split(',')]


def get_all_coords_with_wire_on_them(list_of_instructions: list) -> dict:
    """
    Takes a list of instructions, generates the locations of the lines, and
    stores them in a dictionary. The keys are the locations of wire (as a
    tuple) and the values are a list of times at which the wire was at those
    points.

    Params:
        list_of_instruction (list): The instructions are tuples like: ('U', 3)

    Returns:
        dict of locations the line is at.
    """
    wire_positions = defaultdict(list)
    loc = (0, 0)
    time = 0
    for instruction in list_of_instructions:
        direction = instruction[0]
        distance = instruction[1]
        if direction == 'U':
            increment = (0, 1)
        elif direction == 'L':
            increment = (-1, 0)
        elif direction == 'R':
            increment = (1, 0)
        elif direction == 'D':
            increment = (0, -1)
        for i in range(distance):
            wire_positions[(loc[0] + (i * increment[0]), loc[1] + (i * increment[1]))].append(time)
            time += 1
        loc = (loc[0] + (distance * increment[0]), loc[1] + (distance * increment[1]))
    wire_positions[loc].append(time)
    return dict(wire_positions)


def part_a(wire_paths: list):
    """
    Find all the crossings, then return the manhattan distance of the crossing
    with the smallest manhattan distance to the origin point.
    """
    wire_1_locs = set(get_all_coords_with_wire_on_them(get_instructions_from_string(wire_paths[0])).keys())
    wire_2_locs = set(get_all_coords_with_wire_on_them(get_instructions_from_string(wire_paths[1])).keys())
    crossings = wire_1_locs.intersection(wire_2_locs)
    crossings.remove((0, 0))  # Remove origin point
    crossings = list(crossings)
    m_distances = [abs(x[0]) + abs(x[1]) for x in crossings]
    min_crossing = crossings[m_distances.index(min(m_distances))]
    return (abs(min_crossing[0]) + abs(min_crossing[1]))


def part_b(wire_paths: list):
    """
    Find all the crossings, but at the total combined 'time' for the signal to
    get to the crossing.
    """
    wire_1_dict = get_all_coords_with_wire_on_them(get_instructions_from_string(wire_paths[0]))
    wire_2_dict = get_all_coords_with_wire_on_them(get_instructions_from_string(wire_paths[1]))
    wire_1_locs = set(wire_1_dict.keys())
    wire_2_locs = set(wire_2_dict.keys())
    crossings = wire_1_locs.intersection(wire_2_locs)
    crossings.remove((0, 0))  # Remove origin point
    crossings = list(crossings)
    list_of_combined_times = []
    for crossing in crossings:
        for i in range(len(wire_1_dict[crossing])):
            list_of_combined_times.append(wire_1_dict[crossing][i] + wire_2_dict[crossing][i])
    return min(list_of_combined_times)


if __name__ == "__main__":
    input = read_inputs('input.txt')
    print("Part A: " + str(part_a(input)))
    print("Part B: " + str(part_b(input)))
