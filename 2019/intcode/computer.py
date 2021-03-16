"""
A file containing the computer which is used to run all intcode programs.
"""

from collections import defaultdict
from typing import Callable
import enum

class IntCodeComputerError(enum.IntEnum):
    """ List of possible error codes """
    PROGRAM_TERMINATION = 1
    NO_ERROR = 0
    OPCODE_NOT_FOUND = -1
    OPCODE_ERROR = -2

class IntCodeParamType(enum.IntEnum):
    """ List of parameter types """
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

class IntCodeComputer(object):
    """ The computer for processing intcode programs. """

    def __init__(self) -> None:
        self.program_code = []
        self.opcodes = {}
        self.program_counter = 0
        self.stdinput = []
        self.stdoutput = []

    def set_program_code(self, program_code: list) -> None:
        """
        Sets the program code. It is set with a copy, so to inspect program
        modifications, be sure to get it with get_program_code.
        """
        self.program_code = program_code.copy()

    def get_program_code(self) -> list:
        """ Get's the program code the computer is running. """
        return self.program_code

    def add_opcode(self, opcode: int, function: Callable) -> None:
        """
        Adds an opcode into a dictionary of opcodes. The opcode functions are
        added with the opcode number that correspondes to the function.
        """
        self.opcodes[opcode] = function

    def add_opcodes(self, opcodes: dict) -> None:
        """ Adds a dict of opcodes and corresponding functions at once. """
        for opcode, function in opcodes.items():
            self.opcodes[opcode] = function

    def remove_opcode(self, opcode: int) -> None:
        """ Removes opcodes from the intcode computer """
        del self.opcodes[opcode]

    def specify_input(self, input: int) -> None:
        """ Allows the user to specify input to the opcode computer. """
        self.stdinput.append(input)

    def run(self):
        """ Run the intcode computer until error or termination. """
        while True:
            # Find opcode we are pointing at
            opcode = get_current_opcode(self)
            if opcode not in self.opcodes:
                return IntCodeComputerError.OPCODE_NOT_FOUND

            # Run opcode
            error_code = self.opcodes[opcode](self)
            if error_code != IntCodeComputerError.NO_ERROR:
                return error_code

###############################################################################
#                          Opcode Helper Functions                            #
###############################################################################

def get_parameter_types(computer: IntCodeComputer) -> defaultdict:
    """
    Takes the computer so we can get the current program counter value and a
    number of parameters that we want to check the parameter type for.
    """
    d = defaultdict(int)
    current_intcode = computer.program_code[computer.program_counter]
    padded_incode = str(current_intcode).rjust(2, '0')
    padded_incode = padded_incode[0:-2] # Chop off intcode
    padded_incode = padded_incode[::-1] # Reverse so the rest is in order

    for i in range(len(padded_incode)):
        d[i + 1] = int(padded_incode[i])
    return d

def get_current_opcode(computer: IntCodeComputer) -> int:
    """
    Returns the IntCode of the current instruction.
    """
    current_intcode = computer.program_code[computer.program_counter]
    return int(str(current_intcode)[-2:].rjust(2, '0'))

def get_computer_program_value(computer: IntCodeComputer, offset: int) -> int:
    """
    When accessing a parameter, we can use position mode or immediate mode.
    This function gets the correct number so we don't have to think about it.
    """
    param_type = get_parameter_types(computer)[offset]
    code = computer.program_code
    pc = computer.program_counter
    if param_type == IntCodeParamType.POSITION_MODE:
        return code[code[pc + offset]]
    elif param_type == IntCodeParamType.IMMEDIATE_MODE:
        return code[pc + offset]
    else:
        raise Exception("Non-valid parameter type detected.")

def set_computer_program_value(computer: IntCodeComputer, offset: int, value: int) -> None:
    """
    When setting a parameter, we can only use immediate mode. This function
    ensures we do that. Takes the computer, the offset, and the value to set it
    to.
    """
    param_type = get_parameter_types(computer)[offset]
    code = computer.program_code
    pc = computer.program_counter
    if param_type == IntCodeParamType.POSITION_MODE:
        code[code[pc + offset]] = value
    elif param_type == IntCodeParamType.IMMEDIATE_MODE:
        raise Exception("Can't write to immediate-mode params.")
    else:
        raise Exception("Non-valid parameter type detected.")

###############################################################################
#                                  Opcodes                                    #
###############################################################################

def opcode_add(computer: IntCodeComputer) -> int:
    """
    An opcode instruction that gets the value of the program at the location
    pointed to by pc + 1 and pc + 2, and places the addition of these two into
    the location pointed to by pc + 3. Then jumps the program counter to
    pc + 4.
    """
    param_1 = get_computer_program_value(computer, 1)
    param_2 = get_computer_program_value(computer, 2)
    set_computer_program_value(computer, 3, param_1 + param_2)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR

def opcode_multiply(computer: IntCodeComputer) -> int:
    """
    Same as opcode_add, but multiplies the numbers instead.
    """
    param_1 = get_computer_program_value(computer, 1)
    param_2 = get_computer_program_value(computer, 2)
    set_computer_program_value(computer, 3, param_1 * param_2)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR

def opcode_terminate(computer: IntCodeComputer) -> int:
    """
    If this opcode is received, terminate the program immediately.
    """
    return IntCodeComputerError.PROGRAM_TERMINATION

def opcode_input(computer: IntCodeComputer) -> int:
    """
    Read input from a buffer.
    """
    input = computer.stdinput.pop()
    set_computer_program_value(computer, 1, input)
    computer.program_counter += 2
    return IntCodeComputerError.NO_ERROR

def opcode_output(computer: IntCodeComputer) -> int:
    """
    Write output to a buffer.
    """
    value = get_computer_program_value(computer, 1)
    computer.stdoutput.append(value)
    computer.program_counter += 2
    return IntCodeComputerError.NO_ERROR

def opcode_jump_if_true(computer: IntCodeComputer) -> int:
    value = get_computer_program_value(computer, 1)
    jump_value = get_computer_program_value(computer, 2)
    if value != 0:
        computer.program_counter = jump_value
    else:
        computer.program_counter += 3
    return IntCodeComputerError.NO_ERROR

def opcode_jump_if_false(computer: IntCodeComputer) -> int:
    value = get_computer_program_value(computer, 1)
    jump_value = get_computer_program_value(computer, 2)
    if value == 0:
        computer.program_counter = jump_value
    else:
        computer.program_counter += 3
    return IntCodeComputerError.NO_ERROR

def opcode_jump_if_less_than(computer: IntCodeComputer) -> int:
    param_1 = get_computer_program_value(computer, 1)
    param_2 = get_computer_program_value(computer, 2)
    if param_1 < param_2:
        set_computer_program_value(computer, 3, 1)
    else:
        set_computer_program_value(computer, 3, 0)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR

def opcode_jump_if_equal(computer: IntCodeComputer) -> int:
    param_1 = get_computer_program_value(computer, 1)
    param_2 = get_computer_program_value(computer, 2)
    if param_1 == param_2:
        set_computer_program_value(computer, 3, 1)
    else:
        set_computer_program_value(computer, 3, 0)
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR

DEFAULT_OPCODES = {
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