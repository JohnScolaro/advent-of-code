"""
A file containing the computer which is used to run all intcode programs.
"""

from typing import Callable
import enum

class IntCodeComputerError(enum.Enum):
    """ List of possible error codes """
    PROGRAM_TERMINATION = 1
    NO_ERROR = 0
    OPCODE_NOT_FOUND = -1
    OPCODE_ERROR = -2

class IntCodeComputer(object):
    """ The computer for processing intcode programs. """

    def __init__(self) -> None:
        self.program_code = []
        self.opcodes = {}
        self.program_counter = 0

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

    def run(self):
        """ Run the intcode computer until error or termination. """
        while True:
            # Find opcode we are pointing at
            opcode = self.program_code[self.program_counter]
            if opcode not in self.opcodes:
                return IntCodeComputerError.OPCODE_NOT_FOUND

            # Run opcode
            error_code = self.opcodes[self.program_code[self.program_counter]](self)
            if error_code != IntCodeComputerError.NO_ERROR:
                return error_code


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
    pc = computer.program_counter
    program = computer.program_code
    program[program[pc + 3]] = program[program[pc + 1]] + program[program[pc + 2]]
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR

def opcode_multiply(computer: IntCodeComputer) -> int:
    """
    Same as opcode_add, but multiplies the numbers instead.
    """
    pc = computer.program_counter
    program = computer.program_code
    program[program[pc + 3]] = program[program[pc + 1]] * program[program[pc + 2]]
    computer.program_counter += 4
    return IntCodeComputerError.NO_ERROR

def opcode_terminate(computer: IntCodeComputer) -> int:
    """
    If this opcode is received, terminate the program immediately.
    """
    return IntCodeComputerError.PROGRAM_TERMINATION


DEFAULT_OPCODES = {
    1: opcode_add,
    2: opcode_multiply,
    99: opcode_terminate
}