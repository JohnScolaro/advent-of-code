"""
Problem 7 of the Advent-of-Code 2019
"""

import sys
import os
from typing import List

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer_helpers import day_seven_a_helper
from intcode.computer_helpers import day_seven_b_helper


def read_inputs(filename: str) -> List[int]:
    """
    Reads the input file in as a 'program' for our computer.
    """
    input = []
    with open(filename, 'r') as fp:
        for line in fp:
            input.append(line.strip())
    return [int(x) for x in input[0].split(',')]


if __name__ == "__main__":
    program = read_inputs('input.txt')

    _, largest_output = day_seven_a_helper(program)
    print("Part A: {}".format(largest_output))

    _, largest_output = day_seven_b_helper(program)
    print("Part B: {}".format(largest_output))
