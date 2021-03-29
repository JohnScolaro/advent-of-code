"""
Problem 2 of the Advent-of-Code 2019
"""

import sys
import os
import itertools
from typing import List

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer import IntCodeComputer
from intcode.computer import IntCodeComputerError
from intcode.computer import DEFAULT_OPCODES


def read_inputs(filename: str) -> List[int]:
    """ Reads puzzle input into a list of ints """
    input = []
    with open(filename, 'r') as fp:
        for line in fp:
            input.append(line.strip())
    return [int(x) for x in input[0].split(',')]


def part_a(intcode: list):
    """ Run the intcode computer and return the result for part A """
    computer = IntCodeComputer()
    computer.set_program_code(intcode)
    computer.add_opcodes(DEFAULT_OPCODES)
    retval = computer.run()
    if retval != IntCodeComputerError.PROGRAM_TERMINATION:
        return -1
    else:
        return computer.program_code[0]


def part_b(intcode: list):
    """
    Run the solution for part A through all the different combinations of valid
    verb/noun until one is found that gives the chosen number for part B.
    """
    for noun, verb in itertools.product(range(1, 100), range(1, 100)):
        intcode[1] = noun
        intcode[2] = verb
        result = part_a(intcode)
        if result == 19690720:
            return (100 * noun) + verb


if __name__ == "__main__":
    input = read_inputs('input.txt')
    input[1] = 12
    input[2] = 2
    print("Part A: " + str(part_a(input)))
    print("Part B: " + str(part_b(input)))
