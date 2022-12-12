"""
Problem 24 of the Advent-of-Code 2021
"""

from typing import Callable, List, Optional, Set, Tuple, Union
import dataclasses
from copy import deepcopy

Instruction = Tuple[str, str, str]


@dataclasses.dataclass
class Variable:
    position: int


@dataclasses.dataclass
class Operation:
    left: Union["Operation", int, Variable]
    right: Union["Operation", int, Variable]
    func: Callable[[int, int], int]


def get_callable(operation: str) -> Callable[[int, Optional[int]], int]:
    if operation == "add":
        return lambda x, y: x + y
    elif operation == "mul":
        return lambda x, y: x * y
    elif operation == "div":
        return lambda x, y: x // y
    elif operation == "mod":
        return lambda x, y: x % y
    elif operation == "eql":
        return lambda x, y: int(x == y)
    else:
        raise Exception("Shouldn't get here")


def get_memory_index(variable: str) -> int:
    if variable == "w":
        return 0
    elif variable == "x":
        return 1
    elif variable == "y":
        return 2
    elif variable == "z":
        return 3
    else:
        raise Exception("Shouldn't get here")


def read_inputs(input_file: str) -> List[Instruction]:
    instructions: List[Instruction] = []
    with open(input_file, "r") as fp:
        for line in fp:
            proc_line = line.strip().split()
            instructions.append(tuple(proc_line))
    return instructions


def get_operation_tree(instructions: List[Instruction]) -> List[Operation]:
    memory = [0, 0, 0, 0]
    current_variable_index = 0
    for instruction in instructions:
        if instruction[0] == "inp":
            memory[get_memory_index(instruction[1])] = Variable(position=current_variable_index)
            current_variable_index += 1
        else:
            try:
                left_value = int(instruction[1])
            except ValueError:
                left_value = memory[get_memory_index(instruction[1])]

            try:
                right_value = int(instruction[2])
            except ValueError:
                right_value = memory[get_memory_index(instruction[2])]

            memory[get_memory_index(instruction[1])] = Operation(
                left=left_value,
                right=right_value,
                func=get_callable(instruction[0]),
            )
    return memory


def get_valid_inputs(operation: Operation) -> Set[int]:
    """
    From an operation, we can get a set of numbers that satisfy the requirement
    that that particular operation equals 0 at the end of the program.
    """
    if isinstance(operation.left, int):
        valid_left_inputs = operation.left
    if isinstance(operation.left, Variable):
        valid_left_inputs = {operation.left.position: Set(range(1, 10))}
    else:
        valid_left_inputs = get_valid_inputs(operation.left)

    if isinstance(operation.right, int):
        valid_right_inputs = operation.right
    if isinstance(operation.right, Variable):
        valid_right_inputs = {operation.right.position: Set(range(1, 10))}
    else:
        valid_right_inputs = get_valid_inputs(operation.right)

    return set()


def part_a(operation_tree: List[Operation]) -> int:
    operation_tree = get_operation_tree(instructions)
    final_operation = Operation(left=operation_tree, right=0, func=get_callable("eql"))
    print(final_operation)
    # return get_valid_inputs(final_operation)


def part_b(instructions: List[Instruction]) -> int:
    return 0


if __name__ == "__main__":
    instructions = read_inputs("input.txt")
    operation_tree = get_operation_tree(instructions)
    print(f"Part A: {part_a(instructions)}")
    # print(f"Part B: {part_b(instructions)}")
