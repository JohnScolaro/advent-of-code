"""
Problem 7 of the Advent-of-Code 2019
"""

import sys
import os
from typing import List

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer import day_seven_helper


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
    optimal_phases, largest_output = day_seven_helper(5, program)
    print(largest_output)
    
    


    # print("Part A: {}".format(str(part_a(program))))
    # print("Part B: {}".format(str(part_b(program))))
