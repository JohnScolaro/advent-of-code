import unittest
from computer import opcode_add, opcode_multiply, opcode_terminate
from computer import IntCodeComputer, IntCodeComputerError
from computer import DEFAULT_OPCODES


class TestOpcodeTerminate(unittest.TestCase):
    def test_terminate(self):
        c = IntCodeComputer()
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([99])
        retval = c.run()

        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)


class TestOpcodeAdd(unittest.TestCase):
    def test_basic_add(self):
        c = IntCodeComputer()
        c.add_opcode(1, opcode_add)
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([1,0,0,0,99])
        retval = c.run()

        self.assertEqual([2,0,0,0,99], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)


class TestOpcodeMultiply(unittest.TestCase):
    def test_basic_multiply(self):
        c = IntCodeComputer()
        c.add_opcode(2, opcode_multiply)
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([2,3,0,3,99])
        retval = c.run()
        
        self.assertEqual([2,3,0,6,99], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)

    def test_basic_multiply_2(self):
        c = IntCodeComputer()
        c.add_opcode(2, opcode_multiply)
        c.add_opcode(99, opcode_terminate)
        c.set_program_code([2,4,4,5,99,0])
        retval = c.run()
        
        self.assertEqual([2,4,4,5,99,9801], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)


class TestComputer(unittest.TestCase):
    def test_one(self):
        c = IntCodeComputer()
        c.add_opcodes(DEFAULT_OPCODES)
        c.set_program_code([1,1,1,4,99,5,6,0,99])
        retval = c.run()
        
        self.assertEqual([30,1,1,4,2,5,6,0,99], c.get_program_code())
        self.assertEqual(retval, IntCodeComputerError.PROGRAM_TERMINATION)

if __name__ == '__main__':
    unittest.main()
