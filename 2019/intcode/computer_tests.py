import unittest
from computer import IntCodeComputer
from computer import IntCodeComputerError
from computer import opcode_terminate
from computer import opcode_add
from computer import opcode_multiply
from computer import IntCodeParamType
from computer import get_parameter_types
from computer import get_current_opcode
from computer import get_computer_program_value
from computer import set_computer_program_value
from computer import get_setup_computer
from computer import day_seven_helper
from computer import DEFAULT_OPCODES


class TestOpcodeTerminate(unittest.TestCase):
    def test_terminate(self) -> None:
        c = IntCodeComputer()
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([99])
        retval = c.run()

        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)


class TestOpcodeAdd(unittest.TestCase):
    def test_basic_add(self) -> None:
        c = IntCodeComputer()
        c.add_opcode(1, opcode_add)
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([1, 0, 0, 0, 99])
        retval = c.run()

        self.assertEqual([2, 0, 0, 0, 99], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)


class TestOpcodeMultiply(unittest.TestCase):
    def test_basic_multiply(self) -> None:
        c = IntCodeComputer()
        c.add_opcode(2, opcode_multiply)
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([2, 3, 0, 3, 99])
        retval = c.run()

        self.assertEqual([2, 3, 0, 6, 99], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)

    def test_basic_multiply_2(self) -> None:
        c = IntCodeComputer()
        c.add_opcode(2, opcode_multiply)
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([2, 4, 4, 5, 99, 0])
        retval = c.run()

        self.assertEqual([2, 4, 4, 5, 99, 9801], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)


class TestHelperFunctions(unittest.TestCase):
    def test_get_param_type_immediate(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([11101])
        param_types = get_parameter_types(c)
        self.assertEqual(param_types[1], IntCodeParamType.IMMEDIATE_MODE)
        self.assertEqual(param_types[2], IntCodeParamType.IMMEDIATE_MODE)
        self.assertEqual(param_types[3], IntCodeParamType.IMMEDIATE_MODE)
        self.assertEqual(len(param_types), 3)

    def test_get_param_type_position(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([1])
        param_types = get_parameter_types(c)
        self.assertEqual(param_types[1], IntCodeParamType.POSITION_MODE)
        self.assertEqual(param_types[2], IntCodeParamType.POSITION_MODE)
        self.assertEqual(param_types[3], IntCodeParamType.POSITION_MODE)
        self.assertEqual(len(param_types), 3)

    def test_get_param_type_large(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([10101000101])
        param_types = get_parameter_types(c)
        self.assertEqual(param_types, {1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0, 9: 1})
        self.assertEqual(len(param_types), 9)

    def test_get_param_type_small(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([1])
        param_types = get_parameter_types(c)
        self.assertEqual(param_types, {})

    def test_get_param_type_small_2(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([10])
        param_types = get_parameter_types(c)
        self.assertEqual(param_types, {})
        self.assertEqual(param_types[1], 0)  # Check it's a defaultdict

    def test_get_opcode_1(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([1])
        self.assertEqual(get_current_opcode(c), 1)

    def test_get_opcode_2(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([99])
        self.assertEqual(get_current_opcode(c), 99)

    def test_get_opcode_3(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([101])
        self.assertEqual(get_current_opcode(c), 1)

    def test_program_value_get_position(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([4, 3, 2, 1])
        self.assertEqual(get_computer_program_value(c, 1), 1)

    def test_program_value_get_immediate(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([104, 3, 2, 1])
        self.assertEqual(get_computer_program_value(c, 1), 3)

    def test_program_value_set_position(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([4, 3, 2, 1])
        set_computer_program_value(c, 3, 1)
        self.assertEqual(c.get_program_code(), [4, 1, 2, 1])

    def test_program_value_set_immediate(self) -> None:
        c = IntCodeComputer()
        c.set_program_code([104, 3, 2, 1])
        self.assertRaises(Exception, set_computer_program_value, c, 1, 1)


class TestComputerDay2(unittest.TestCase):
    def test_one(self) -> None:
        program = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        c = get_setup_computer(program, None, DEFAULT_OPCODES)
        retval = c.run()

        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)

    def test_two(self) -> None:
        """
        This is the Day 2 part A question.
        """
        program = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 19, 5, 23, 1, 13, 23, 27, 1, 27, 6, 31, 2, 31, 6, 35, 2, 6, 35, 39, 1, 39, 5, 43, 1, 13, 43, 47, 1, 6, 47, 51, 2, 13, 51, 55, 1, 10, 55, 59, 1, 59, 5, 63, 1, 10, 63, 67, 1, 67, 5, 71, 1, 71, 10, 75, 1, 9, 75, 79, 2, 13, 79, 83, 1, 9, 83, 87, 2, 87, 13, 91, 1, 10, 91, 95, 1, 95, 9, 99, 1, 13, 99, 103, 2, 103, 13, 107, 1, 107, 10, 111, 2, 10, 111, 115, 1, 115, 9, 119, 2, 119, 6, 123, 1, 5, 123, 127, 1, 5, 127, 131, 1, 10, 131, 135, 1, 135, 6, 139, 1, 10, 139, 143, 1, 143, 6, 147, 2, 147, 13, 151, 1, 5, 151, 155, 1, 155, 5, 159, 1, 159, 2, 163, 1, 163, 9, 0, 99, 2, 14, 0, 0]  # noqa: E501
        c = get_setup_computer(program, None, DEFAULT_OPCODES)
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.get_program_code()[0], 4690667)


class TestComputerDay5(unittest.TestCase):
    def test_part_a_one(self) -> None:
        """
        This test should output whatever we input.
        """
        c = get_setup_computer([3, 0, 4, 0, 99], 69, DEFAULT_OPCODES)
        retval = c.run()

        self.assertEqual(c.stdoutput[0], 69)
        self.assertEqual(len(c.stdoutput), 1)
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)

    def test_part_a_two(self) -> None:
        """
        This test should multiply 33 by 3 then place it in 4. This is 99 and terminates
        the program immediately.
        """
        c = get_setup_computer([1002, 4, 3, 4, 33], None, DEFAULT_OPCODES)
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)

    def test_part_a_three(self) -> None:
        """
        This test is day 5 part A.
        """
        program = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 65, 73, 225, 1101, 37, 7, 225, 1101, 42, 58, 225, 1102, 62, 44, 224, 101, -2728, 224, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 223, 224, 223, 1, 69, 126, 224, 101, -92, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 7, 224, 224, 1, 223, 224, 223, 1102, 41, 84, 225, 1001, 22, 92, 224, 101, -150, 224, 224, 4, 224, 102, 8, 223, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1101, 80, 65, 225, 1101, 32, 13, 224, 101, -45, 224, 224, 4, 224, 102, 8, 223, 223, 101, 1, 224, 224, 1, 224, 223, 223, 1101, 21, 18, 225, 1102, 5, 51, 225, 2, 17, 14, 224, 1001, 224, -2701, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224, 223, 101, 68, 95, 224, 101, -148, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 1, 224, 224, 1, 223, 224, 223, 1102, 12, 22, 225, 102, 58, 173, 224, 1001, 224, -696, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 6, 224, 1, 223, 224, 223, 1002, 121, 62, 224, 1001, 224, -1302, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 1008, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 329, 1001, 223, 1, 223, 7, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 1001, 223, 1, 223, 1007, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 359, 1001, 223, 1, 223, 1007, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 374, 1001, 223, 1, 223, 108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 389, 101, 1, 223, 223, 8, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 404, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 419, 101, 1, 223, 223, 8, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 434, 101, 1, 223, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 449, 101, 1, 223, 223, 7, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 464, 101, 1, 223, 223, 1107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 479, 1001, 223, 1, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 494, 101, 1, 223, 223, 108, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 509, 101, 1, 223, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 524, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 539, 101, 1, 223, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 554, 101, 1, 223, 223, 8, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 569, 101, 1, 223, 223, 107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 584, 101, 1, 223, 223, 1108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 599, 1001, 223, 1, 223, 1008, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 614, 101, 1, 223, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 629, 101, 1, 223, 223, 1108, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 644, 1001, 223, 1, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 659, 1001, 223, 1, 223, 108, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 674, 101, 1, 223, 223, 4, 223, 99, 226]  # noqa: E501
        c = get_setup_computer(program, 1, DEFAULT_OPCODES)
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput[-1], 14522484)

    def test_part_b_one(self) -> None:
        """
        Using position mode, consider whether the input is equal to 8; output 1
        (if it is) or 0 (if it is not).
        """
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        c = get_setup_computer(program, 8, DEFAULT_OPCODES)  # 8 == 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1])

        c = get_setup_computer(program, 0, DEFAULT_OPCODES)  # 0 != 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [0])

    def test_part_b_two(self) -> None:
        """
        Using position mode, consider whether the input is less than 8; output
        1 (if it is) or 0 (if it is not).
        """
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        c = get_setup_computer(program, 7, DEFAULT_OPCODES)  # Input < 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1])

        c = get_setup_computer(program, 8, DEFAULT_OPCODES)  # Input ! < 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [0])

    def test_part_b_three(self) -> None:
        """
        Using immediate mode, consider whether the input is equal to 8; output
        1 (if it is) or 0 (if it is not).
        """
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        c = get_setup_computer(program, 8, DEFAULT_OPCODES)  # Input == 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1])

        c = get_setup_computer(program, 0, DEFAULT_OPCODES)  # Input != 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [0])

    def test_part_b_four(self) -> None:
        """
        Using immediate mode, consider whether the input is less than 8; output
        1 (if it is) or 0 (if it is not).
        """
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        c = get_setup_computer(program, 7, DEFAULT_OPCODES)  # Input < 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1])

        c = get_setup_computer(program, 8, DEFAULT_OPCODES)  # Input ! < 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [0])

    def test_part_b_five(self) -> None:
        """
        Here is a jump test that take an input, then output 0 if the input was
        zero or 1 if the input was non-zero. This one uses position mode.
        """
        program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        c = get_setup_computer(program, 0, DEFAULT_OPCODES)  # Input == 0
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [0])

        c = get_setup_computer(program, 69, DEFAULT_OPCODES)  # Input != 0
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1])

    def test_part_b_six(self) -> None:
        """
        Here is a jump test that take an input, then output 0 if the input was
        zero or 1 if the input was non-zero. This one uses immediate mode.
        """
        program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        c = get_setup_computer(program, 0, DEFAULT_OPCODES)  # Input == 0
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [0])

        c = get_setup_computer(program, 69, DEFAULT_OPCODES)  # Input != 0
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1])

    def test_part_b_seven(self) -> None:
        """
        Here is a jump test that take an input, then output 0 if the input was
        zero or 1 if the input was non-zero. This one uses immediate mode.
        """
        original_program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]  # noqa: E501

        c = get_setup_computer(original_program, 7, DEFAULT_OPCODES)  # Input < 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [999])

        c = get_setup_computer(original_program, 8, DEFAULT_OPCODES)  # Input == 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1000])

        c = get_setup_computer(original_program, 9, DEFAULT_OPCODES)  # Input > 8
        retval = c.run()
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)
        self.assertEqual(c.stdoutput, [1001])


class TestComputerDay7(unittest.TestCase):

    def test_a_one(self) -> None:
        program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
        optimal_phases, largest_output = day_seven_helper(5, program)
        self.assertEqual([4, 3, 2, 1, 0], optimal_phases)
        self.assertEqual(largest_output, 43210)

    def test_a_two(self) -> None:
        program = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
        optimal_phases, largest_output = day_seven_helper(5, program)
        self.assertEqual([0, 1, 2, 3, 4], optimal_phases)
        self.assertEqual(largest_output, 54321)

    def test_a_three(self) -> None:
        program = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]  # noqa: E501
        optimal_phases, largest_output = day_seven_helper(5, program)
        self.assertEqual([1, 0, 4, 3, 2], optimal_phases)
        self.assertEqual(largest_output, 65210)


if __name__ == '__main__':
    unittest.main()
