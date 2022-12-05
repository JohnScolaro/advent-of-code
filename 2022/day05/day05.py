"""
Problem 5 of the Advent-of-Code 2022
"""

from typing import Any, List
from copy import deepcopy


def read_inputs(filename: str) -> tuple[list[list[tuple[str]]], list[tuple[int]]]:
    input_list = []
    with open(filename, "r") as fp:
        state = list(zip(*[next(fp), next(fp), next(fp), next(fp), next(fp), next(fp), next(fp), next(fp)]))
        next(fp)
        next(fp)
        instructions = [line.strip() for line in fp]

    state = [state[1], state[5], state[9], state[13], state[17], state[21], state[25], state[29], state[33]]
    state = list(map(list, state))
    state = [[element for element in pile if element != ' '] for pile in state]
    for pile in state:
        pile.reverse()

    instructions = [(int(instruction.split()[1]), int(instruction.split()[3]), int(instruction.split()[5])) for instruction in instructions]

    return state, instructions


def part_a(input_list: tuple[list[list[tuple[str]]], list[tuple[int]]]) -> str:
    state, instructions = input_list
    state = deepcopy(state)
    
    for num_moves, from_loc, to_loc in instructions:
        for i in range(num_moves):
            package = state[from_loc - 1].pop(-1)
            state[to_loc - 1].append(package)

    return ''.join(pile[-1] for pile in state)


def part_b(input_list: tuple[list[list[tuple[str]]], list[tuple[int]]]) -> str:
    state, instructions = input_list
    state = deepcopy(state)
    
    for num_moves, from_loc, to_loc in instructions:

        a = []
        for i in range(num_moves):
            a.append(state[from_loc - 1].pop(-1))

        for i in range(num_moves):
            state[to_loc - 1].append(a.pop(-1))

    return ''.join(pile[-1] for pile in state)


if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {part_a(input_list)}")
    print(f"Part B: {part_b(input_list)}")
