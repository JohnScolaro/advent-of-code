"""
Solutions for the Advent of Code - Day 18

Alright to anyone reading this, I need to explain...
I know that to parse equations PROPERLY I should be making a tree of
expressions, and then you recursively call evaluate() on the top node which
recursively evaluates all the nested nodes all the way down. Sure. Boring.

What's WAY more fun however, it to try to do it all with a dumb stack
calculator. For part A, it's easy. For part B, it's impossible, so I hacked a
dumb 'equation modifier' to modify the equation by adding brackets so that
the stack calculator actually CAN parse it.
"""

def read_input(file_name: str):
    """ Reads input into a list of strings. Removes whitespace. """
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            l.append(line.strip().replace(' ', ''))
    return l

def part_a_stack_calculator(equation: str):
    """ A stack calculator for solving part A """
    # 'Stacks' for keeping track of current operator and running value
    number_stack = []
    operator_stack = []

    # Starting operator is + so first number gets added to starting value of 0
    current_operator = '+'
    current_value = 0

    for char in equation:
        # If we run into a number, do the calculation according to the last
        # operator we encountered.
        if char.isdigit():
            if current_operator == '*':
                current_value *= int(char)
            elif current_operator == '+':
                current_value += int(char)

        # If we start a bracket, we push our running value and last operator
        # onto the stacks, and start fresh inside the brackets.
        elif char == '(':
            operator_stack.append(current_operator)
            current_operator = '+'
            number_stack.append(current_value)
            current_value = 0

        # When we leave brackets, carry the entire bracket total through and
        # apply as if it was a number to the values on the top of the stack.
        elif char == ')':
            current_operator = operator_stack.pop()
            if current_operator == '*':
                current_value = current_value * number_stack.pop()
            if current_operator == '+':
                current_value = current_value + number_stack.pop()
        
        elif char == '+':
            current_operator = '+'
        elif char == '*':
            current_operator = '*'

    return current_value

def part_b_equation_modifier(equation: str) -> str:
    """
    Modifies the equation strings from the input so that when parsed by the
    dumb stack calculator I made, they actually evaluate correctly. Essentially
    this function just adds brackets to the string to make it work.

    The rules it follows are:
        1: Copy the origional letter from the input string.
        2: If the char is a *, add an open parenthesis after it, and keep
            track of this additional parenthesis you added.
        3: If the char is a (, push number of addition brackets you've added
            at this specific level to a stack.
        4: If the char is a ), insert X additional ')'s to the equation, where
            X is the total number of extra '('s you've added at this particular
            parenthesis level.

    It's dumb, and I thought it up by attempting a few equations by hand, and
    it just kinda seemed like it would work.
    """
    string = ''
    brackets_added = 0
    num_additional_brackets = []
    for char in equation:
        string += char
        if char == '*':
            string += '('
            brackets_added += 1
        if char == '(':
            num_additional_brackets.append(brackets_added)
            brackets_added = 0
        if char == ')':
            string += ')' * brackets_added
            brackets_added = num_additional_brackets.pop()
    string += ')' * brackets_added
    return string

def part_a(all_equations: list) -> int:
    sum_of_all_equations = 0
    for equation in all_equations:
        sum_of_all_equations += part_a_stack_calculator(equation)
    return sum_of_all_equations

def part_b(all_equations: list) -> int:
    sum_of_all_equations = 0
    for equation in all_equations:
        sum_of_all_equations += part_a_stack_calculator(part_b_equation_modifier(equation))
    return sum_of_all_equations

if __name__ == "__main__":
    all_equations = read_input('input.txt')
    print("Part A: " + str(part_a(all_equations)))
    print("Part B: " + str(part_b(all_equations)))