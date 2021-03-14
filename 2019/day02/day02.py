"""
Problem 2 of the Advent-of-Code 2019
"""

import sys, os
import itertools

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer import IntCodeComputer, IntCodeComputerError
from intcode.computer import DEFAULT_OPCODES

def read_inputs(filename: str) -> list:
    """ Reads puzzle input into a list of ints """
    l = []
    with open(filename, 'r') as fp:
        for line in fp:
            l.append(line.strip())
    l = [int(x) for x in l[0].split(',')]
    return l

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
    l = read_inputs('input.txt')
    print("Part A: " + str(part_a(l)))
    print("Part B: " + str(part_b(l)))
    