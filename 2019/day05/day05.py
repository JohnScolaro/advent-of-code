"""
Problem 5 of the Advent-of-Code 2019

Another intcode problem. Uses the previously created intcode computer.
"""

import sys, os
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer import IntCodeComputer, IntCodeComputerError
from intcode.computer import DEFAULT_OPCODES

def read_program(filename: str) -> list:
    """
    Read the input file and return the program as a list of ints.
    """
    l = []
    with open(filename, 'r') as fp:
        for line in fp:
            l.append(line.strip())
    return [int(x) for x in l[0].split(',')]

def part_a(filename: str) -> str:
    program = read_program(filename)
    c = IntCodeComputer()
    c.set_program_code(program)
    c.add_opcodes(DEFAULT_OPCODES)
    c.specify_input(1)
    c.run()
    return str(c.stdoutput[-1])

def part_b(filename: str) -> str:
    program = read_program(filename)
    c = IntCodeComputer()
    c.set_program_code(program)
    c.add_opcodes(DEFAULT_OPCODES)
    c.specify_input(5)
    c.run()
    return str(c.stdoutput[-1])

if __name__ == "__main__":
    print("Part A: {}".format(part_a('input.txt')))
    print("Part B: {}".format(part_b('input.txt')))
