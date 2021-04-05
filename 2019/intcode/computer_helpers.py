"""
A file used to house helper functions related to the intcode computer used in
the advent of code 2019.
"""

import sys
import os
import itertools
import concurrent.futures
from queue import Empty
from typing import Callable, Dict, List, Union, Tuple

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer import IntCodeComputer
from intcode.computer import IntCodeComputerError
from intcode.opcodes import DEFAULT_OPCODES


def get_setup_computer(
        program: List[int],
        input: Union[List[int], int, None],
        opcodes: Dict[int, Callable[[IntCodeComputer], IntCodeComputerError]]
        ) -> IntCodeComputer:
    """
    Returns a setup computer, with program, opcodes, and input all already
    set up. This stops be re-writing the same bunch of lines repeatedly and
    replaces them all with this one.
    """
    c = IntCodeComputer()
    c.set_program_code(program)
    c.add_opcodes(opcodes)
    if input is not None:
        c.specify_input(input)
    return c


def computer_runner(computer: IntCodeComputer) -> None:
    """
    A wrapper around c.run() so that we can call it with a map function.
    """
    computer.run()


def day_seven_a_helper(program: List[int]) -> Tuple[List[int], int]:
    """
    Basically solves day 7a's question. Returns a tuple containing a list which
    is the order of the phases, and an int which is the final output.
    """
    largest_output = 0
    largest_phase_combination = [0]
    for phases in itertools.permutations(list(range(5))):
        input = 0
        for phase in phases:
            c = get_setup_computer(program, [phase, input], DEFAULT_OPCODES)
            retval = c.run()
            if retval != IntCodeComputerError.PROGRAM_TERMINATION:
                raise Exception("Program terminated with Error Code: {}".format(retval))
            input = c.stdoutput.get()
        if input > largest_output:
            largest_output = input
            largest_phase_combination = list(phases)
    return (largest_phase_combination, largest_output)


def day_seven_b_helper(program: List[int]) -> Tuple[List[int], int]:
    """
    Basically solves day 7b's question. Returns a tuple containing a list which
    is the order of the phases and the int which is the final output.
    """
    largest_output = 0
    largest_phase_combination = [0]
    for phases in itertools.permutations(list(range(5, 10))):
        computers: List[IntCodeComputer] = []
        for phase in phases:
            computers.append(get_setup_computer(program, phase, DEFAULT_OPCODES))

        # Plug all the computers into eachother.
        for i in range(5):
            computers[i].specify_queues(computers[i].stdinput, computers[(i + 1) % 5].stdinput)

        # Initial input
        computers[0].stdinput.put(0)

        # Run all threads
        with concurrent.futures.ThreadPoolExecutor(5) as executor:
            executor.map(computer_runner, computers)

        # Get last output from stdout
        while True:
            try:
                output = computers[4].stdoutput.get(block=False)
            except Empty:
                break

        # Computer output to see if it's the largest so far.
        if output > largest_output:
            largest_output = output
            largest_phase_combination = list(phases)
            
    return (largest_phase_combination, largest_output)
