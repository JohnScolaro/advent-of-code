"""
Solutions for the Advent of Code - Day 8
"""

class State(object):
    def __init__(self):
        self.pc = 0
        self.acc = 0

def get_list_of_instructions(input_file: str) -> list:
    """ Reads the input file into a list of strings """
    list_of_instructions = []
    with open(input_file, 'r') as fb:
        for line in fb:
            list_of_instructions.append(line[:-1])
    return list_of_instructions

def execute_instruction(instruction: str, state):
    """ Executes an instruction modifying the state of the machine """
    operation = instruction[:3]
    param = int(instruction[4:])

    if (operation == 'nop'):
       state.pc += 1
    
    if (operation == 'acc'):
        state.pc += 1
        state.acc += param

    if (operation == 'jmp'):
        state.pc += param

def run_until_first_repeat(list_of_instructions: list, state) -> int:
    """ Run until the first time an instruction would otherwise repeat """
    executed_instructions = []
    while True:
        executed_instructions.append(state.pc)
        execute_instruction(list_of_instructions[state.pc], state)
        if state.pc in executed_instructions:
            return

def find_acc_at_end_of_fixed_program(list_of_instructions: list) -> int:
    """
    Attempt to fix the program. When it finishes successfully, return the acc.
    """
    fix_num = 0
    while True:
        possible_fixed_program = get_fixed_instructions(list_of_instructions, fix_num)
        state = State()
        try:
            run_until_first_repeat(possible_fixed_program, state)
        except:
            return state.acc

        fix_num += 1
        

def get_fixed_instructions(list_of_instructions: list, i: int) -> list:
    """Returns a fixed list of instructions.

    Attempts the i'th possible fix to the instructions and returns the fixed
    list.
    """
    possible_change = 0
    fixed_list_of_instructions = []

    for instruction in list_of_instructions:
        operation = instruction[:3]

        if operation == 'nop':
            if possible_change == i:
                instruction = 'jmp' + instruction[3:]
            possible_change += 1
        elif operation == 'jmp':
            if possible_change == i:
                instruction = 'nop' + instruction[3:]
            possible_change += 1
        fixed_list_of_instructions.append(instruction)

    return fixed_list_of_instructions

if __name__ == "__main__":
    list_of_instructions = get_list_of_instructions('input.txt')
    
    # Part A
    state = State()
    run_until_first_repeat(list_of_instructions, state)
    print(state.acc)
    
    # Part B
    print(find_acc_at_end_of_fixed_program(list_of_instructions))