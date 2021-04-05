"""
This file contains all the different opcodes for the intcode computer used in
the 2019 advent of code.
"""


import sys
import os
from typing import Callable, Dict

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.computer import IntCodeComputer
from intcode.computer import IntCodeComputerError


def opcode_add(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    An opcode instruction that gets the value of the program at the location
    pointed to by pc + 1 and pc + 2, and places the addition of these two into
    the location pointed to by pc + 3. Then jumps the program counter to
    pc + 4.
    """
    param_1 = computer.get_computer_program_value(1)
    param_2 = computer.get_computer_program_value(2)
    computer.set_computer_program_value(3, param_1 + param_2)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR


def opcode_multiply(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Same as opcode_add, but multiplies the numbers instead.
    """
    param_1 = computer.get_computer_program_value(1)
    param_2 = computer.get_computer_program_value(2)
    computer.set_computer_program_value(3, param_1 * param_2)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR


def opcode_terminate(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    If this opcode is received, terminate the program immediately.
    """
    return IntCodeComputerError.PROGRAM_TERMINATION


def opcode_input(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Read input from a buffer.
    """
    input = computer.stdinput.get(block=True, timeout=1.0)
    computer.set_computer_program_value(1, input)
    computer.program_counter += 2
    return IntCodeComputerError.NO_ERROR


def opcode_output(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Write output to a buffer.
    """
    value = computer.get_computer_program_value(1)
    computer.stdoutput.put(value)
    computer.program_counter += 2
    return IntCodeComputerError.NO_ERROR


def opcode_jump_if_true(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Jumps the program counter to a different location if value != 0.
    """
    value = computer.get_computer_program_value(1)
    jump_value = computer.get_computer_program_value(2)
    if value != 0:
        computer.program_counter = jump_value
    else:
        computer.program_counter += 3
    return IntCodeComputerError.NO_ERROR


def opcode_jump_if_false(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Jumps if the value is 0.
    """
    value = computer.get_computer_program_value(1)
    jump_value = computer.get_computer_program_value(2)
    if value == 0:
        computer.program_counter = jump_value
    else:
        computer.program_counter += 3
    return IntCodeComputerError.NO_ERROR


def opcode_jump_if_less_than(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Jumps if a value is less than another value.
    """
    param_1 = computer.get_computer_program_value(1)
    param_2 = computer.get_computer_program_value(2)
    if param_1 < param_2:
        computer.set_computer_program_value(3, 1)
    else:
        computer.set_computer_program_value(3, 0)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR


def opcode_jump_if_equal(computer: IntCodeComputer) -> IntCodeComputerError:
    """
    Jumps if values are equal.
    """
    param_1 = computer.get_computer_program_value(1)
    param_2 = computer.get_computer_program_value(2)
    if param_1 == param_2:
        computer.set_computer_program_value(3, 1)
    else:
        computer.set_computer_program_value(3, 0)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR


DEFAULT_OPCODES: Dict[int, Callable[[IntCodeComputer], IntCodeComputerError]] = {
    1: opcode_add,
    2: opcode_multiply,
    3: opcode_input,
    4: opcode_output,
    5: opcode_jump_if_true,
    6: opcode_jump_if_false,
    7: opcode_jump_if_less_than,
    8: opcode_jump_if_equal,
    99: opcode_terminate
}
