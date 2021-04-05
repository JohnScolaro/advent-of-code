"""
A file containing the computer which is used to run all intcode programs.
"""

from __future__ import annotations
from collections import defaultdict
from typing import Callable, Dict, List, Union, DefaultDict
import enum
import queue


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
        self.program_code: List[int] = []
        self.opcodes: Dict[int, Callable[[IntCodeComputer], IntCodeComputerError]] = {}
        self.program_counter: int = 0
        self.stdinput: queue.Queue[int] = queue.Queue()
        self.stdoutput: queue.Queue[int] = queue.Queue()
        self.termination_value = IntCodeComputerError.NO_ERROR

    def set_program_code(self, program_code: List[int]) -> None:
        """
        Sets the program code. It is set with a copy, so to inspect program
        modifications, be sure to get it with get_program_code.
        """
        self.program_code = program_code.copy()

    def get_program_code(self) -> List[int]:
        """ Returns the program code the computer is running. """
        return self.program_code

    def add_opcode(self, opcode: int, function: Callable[[IntCodeComputer], IntCodeComputerError]) -> None:
        """
        Adds an opcode into a dictionary of opcodes. The opcode functions are
        added with the opcode number that correspondes to the function.
        """
        self.opcodes[opcode] = function

    def add_opcodes(self, opcodes: Dict[int, Callable[[IntCodeComputer], IntCodeComputerError]]) -> None:
        """ Adds a dict of opcodes and corresponding functions at once. """
        for opcode, function in opcodes.items():
            self.opcodes[opcode] = function

    def remove_opcode(self, opcode: int) -> None:
        """ Removes opcodes from the intcode computer """
        del self.opcodes[opcode]

    def specify_input(self, input: Union[List[int], int]) -> None:
        """ Allows the user to specify input to the opcode computer. """
        if isinstance(input, list):
            for item in input:
                self.stdinput.put(item)
        elif isinstance(input, int):
            self.stdinput.put(input)
        else:
            raise TypeError("Expected a list or an int.")

    def specify_queues(self, stdin: queue.Queue[int], stdout: queue.Queue[int]) -> None:
        """
        Used if you don't want to use the default queues. Allows you to connect
        computers together.
        """
        self.stdinput = stdin
        self.stdoutput = stdout

    def get_current_opcode(self) -> int:
        """
        Returns the IntCode of the current instruction.
        """
        current_intcode = self.program_code[self.program_counter]
        return int(str(current_intcode)[-2:].rjust(2, '0'))

    def get_parameter_types(self) -> DefaultDict[int, IntCodeParamType]:
        """
        Takes the computer so we can get the current program counter value and a
        number of parameters that we want to check the parameter type for.
        """
        def get_default_param() -> IntCodeParamType:
            return IntCodeParamType.POSITION_MODE

        d: DefaultDict[int, IntCodeParamType] = defaultdict(get_default_param)
        current_intcode = self.program_code[self.program_counter]
        padded_intcode = str(current_intcode).rjust(2, '0')
        padded_intcode = padded_intcode[0:-2]  # Chop off intcode
        padded_intcode = padded_intcode[::-1]  # Reverse so the rest is in order

        for i in range(len(padded_intcode)):
            d[i + 1] = IntCodeParamType.IMMEDIATE_MODE if int(padded_intcode[i]) else IntCodeParamType.POSITION_MODE
        return d

    def get_computer_program_value(self, offset: int) -> int:
        """
        When accessing a parameter, we can use position mode or immediate mode.
        This function gets the correct number so we don't have to think about it.
        """
        param_type = self.get_parameter_types()[offset]
        code = self.program_code
        pc = self.program_counter
        if param_type == IntCodeParamType.POSITION_MODE:
            return code[code[pc + offset]]
        elif param_type == IntCodeParamType.IMMEDIATE_MODE:
            return code[pc + offset]
        else:
            raise Exception("Non-valid parameter type detected.")

    def set_computer_program_value(self, offset: int, value: int) -> None:
        """
        When setting a parameter, we can only use immediate mode. This function
        ensures we do that. Takes the computer, the offset, and the value to set it
        to.
        """
        param_type = self.get_parameter_types()[offset]
        code = self.program_code
        pc = self.program_counter
        if param_type == IntCodeParamType.POSITION_MODE:
            code[code[pc + offset]] = value
        elif param_type == IntCodeParamType.IMMEDIATE_MODE:
            raise Exception("Can't write to immediate-mode params.")
        else:
            raise Exception("Non-valid parameter type detected.")

    def run(self) -> IntCodeComputerError:
        """ Run the intcode computer until error or termination. """
        while True:
            # Find opcode we are pointing at
            opcode = self.get_current_opcode()
            if opcode not in self.opcodes:
                self.termination_value = IntCodeComputerError.OPCODE_NOT_FOUND
                return IntCodeComputerError.OPCODE_NOT_FOUND

            # Run opcode
            error_code = self.opcodes[opcode](self)
            if error_code != IntCodeComputerError.NO_ERROR:
                self.termination_value = error_code
                return error_code
