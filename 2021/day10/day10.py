"""
Problem 10 of the Advent-of-Code 2019
"""
from typing import Any, Dict, List, Optional, Set, Tuple
from functools import reduce

scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
opening_mapping = {")": "(", "]": "[", "}": "{", ">": "<"}
closing_mapping = {v: k for k, v in opening_mapping.items()}
autocomplete = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def read_inputs(filename: str) -> List[Any]:
    lines = []
    with open(filename, "r") as fp:
        for line in fp:
            lines.append(line.strip())
    return lines


def get_score_of_line(line):
    stack = []
    for char in line:
        if char not in scores:
            stack.append(char)
        else:
            if stack[-1] == opening_mapping[char]:
                stack.pop(-1)
            else:
                return scores[char]
    return 0


def get_stack_at_end_of_incomplete_line(line):
    stack = []
    for char in line:
        if char not in scores:
            stack.append(char)
        else:
            if stack[-1] == opening_mapping[char]:
                stack.pop(-1)
    return stack


def part_a(lines) -> int:
    return sum(map(get_score_of_line, lines))


def part_b(inputs) -> int:
    corrupted_lines = [line for line in inputs if get_score_of_line(line) == 0]
    scores = []
    for line in corrupted_lines:
        stack = get_stack_at_end_of_incomplete_line(line)
        points = reversed([autocomplete[closing_mapping[x]] for x in stack])
        i = 0
        for p in points:
            i *= 5
            i += p
        scores.append(i)
    print(scores)
    print(len(scores))
    print(len(scores) // 2)
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    lines = read_inputs("input.txt")
    print(f"Part A: {part_a(lines)}")
    print(f"Part B: {part_b(lines)}")
