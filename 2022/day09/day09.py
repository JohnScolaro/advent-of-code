"""
Problem 9 of the Advent-of-Code 2022
"""

from typing import Any, List
import more_itertools
from collections import Counter

DIRECTIONS = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

def read_inputs(filename: str) -> List[tuple[tuple[int, int], int]]:
    instructions = []
    with open(filename, "r") as fp:
        for line in fp:
            dir, num = line.strip().split()
            instructions.append((DIRECTIONS[dir], int(num)))
    return instructions

def both_parts(instructions: List[tuple[tuple[int, int], int]], length_of_rope: int) -> int:
    rope_state = [(0, 0) for _ in range(length_of_rope)]
    locs = {}
    locs[rope_state[-1]] = locs.get(rope_state[-1], 0) + 1

    for direction, num_moves in instructions:
        for _ in range(num_moves):
            x_dir, y_dir = direction
            rope_state[0] = (rope_state[0][0]+x_dir, rope_state[0][1] + y_dir)
            for i, (head, tail) in enumerate(more_itertools.windowed(rope_state, 2)):
                rope_state[i+1] = calculate_tail_position(tail, head)
            locs[rope_state[-1]] = locs.get(rope_state[-1], 0) + 1

    return len(locs)

def calculate_tail_position(old_tail_position, new_head_position):
    t_x, t_y = old_tail_position
    h_x, h_y = new_head_position
    if abs(h_x - t_x) <= 1 and abs(h_y - t_y) <= 1:
        return old_tail_position

    new_tail_x = t_x
    new_tail_y = t_y
    if h_x > t_x:
        new_tail_x += 1
    if h_x < t_x:
        new_tail_x -= 1
    if h_y > t_y:
        new_tail_y += 1
    if h_y < t_y:
        new_tail_y -= 1
    
    return (new_tail_x, new_tail_y)

if __name__ == "__main__":
    input_list = read_inputs("input.txt")
    print(f"Part A: {both_parts(input_list, 2)}")
    print(f"Part B: {both_parts(input_list, 10)}")
