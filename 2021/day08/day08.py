"""
Problem 8 of the Advent-of-Code 2019
"""

import itertools
from typing import Any, Dict, List, Set, Tuple
from collections import defaultdict

could_be_in_n_digit_number = {
    2: {"c", "f"},
    3: {"a", "c", "f"},
    4: {"b", "c", "d", "f"},
    5: {"a", "b", "c", "d", "e", "f", "g"},
    6: {"a", "b", "c", "d", "e", "f", "g"},
    7: {"a", "b", "c", "d", "e", "f", "g"},
}

all_five_digit_inputs = {"a", "d", "g"}
some_five_digit_inputs = {"b", "c", "e", "f"}
all_six_digit_inputs = {"a", "b", "f", "g"}
some_six_digit_inputs = {"c", "d", "e"}


def read_inputs(filename: str) -> List[Any]:
    inputs = []
    with open(filename, "r") as fp:
        for line in fp:
            in_out = line.split(" | ")
            i = in_out[0].split()
            o = in_out[1].split()
            inputs.append((i, o))
    return inputs


def get_mapping(observed_inputs: List[str]) -> Dict[str, str]:
    """
    Get the mapping from the observed segment, to the segment it is supposed to be.
    """
    segments = {"a", "b", "c", "d", "e", "f", "g"}
    possible_numbers = {seg: {"a", "b", "c", "d", "e", "f", "g"} for seg in segments}
    for observed_input in observed_inputs:
        for letter in observed_input:
            possible_numbers[letter] = possible_numbers[letter].intersection(
                could_be_in_n_digit_number[len(observed_input)]
            )
    five_digit_inputs = [set(observed_input) for observed_input in observed_inputs if len(observed_input) == 5]
    six_digit_inputs = [set(observed_input) for observed_input in observed_inputs if len(observed_input) == 6]
    segments_in_all_five_digit_inputs = five_digit_inputs[0].intersection(*five_digit_inputs[1:])
    segments_in_some_five_digit_inputs = (
        five_digit_inputs[0].union(*five_digit_inputs[1:]) - segments_in_all_five_digit_inputs
    )
    segments_in_all_six_digit_inputs = six_digit_inputs[0].intersection(*six_digit_inputs[1:])
    segments_in_some_six_digit_inputs = (
        six_digit_inputs[0].union(*six_digit_inputs[1:]) - segments_in_all_six_digit_inputs
    )

    for segment in segments_in_all_five_digit_inputs:
        possible_numbers[segment] = possible_numbers[segment].intersection(all_five_digit_inputs)
    for segment in segments_in_some_five_digit_inputs:
        possible_numbers[segment] = possible_numbers[segment].intersection(some_five_digit_inputs)
    for segment in segments_in_all_six_digit_inputs:
        possible_numbers[segment] = possible_numbers[segment].intersection(all_six_digit_inputs)
    for segment in segments_in_some_six_digit_inputs:
        possible_numbers[segment] = possible_numbers[segment].intersection(some_six_digit_inputs)

    for seg in possible_numbers:
        if len(possible_numbers[seg]) == 1:
            (seg_value,) = possible_numbers[seg]
            for another_seg in possible_numbers:
                if another_seg != seg:
                    possible_numbers[another_seg].discard(seg_value)

    definite_numbers = {k: next(iter(v)) for k, v in possible_numbers.items()}
    return definite_numbers


def match_segments_to_final_number(segments: Set[str]) -> int:
    number_to_segments_mapping = {
        0: {"a", "b", "c", "e", "f", "g"},
        1: {"c", "f"},
        2: {"a", "c", "d", "e", "g"},
        3: {"a", "c", "d", "f", "g"},
        4: {"b", "c", "d", "f"},
        5: {"a", "b", "d", "f", "g"},
        6: {"a", "b", "d", "e", "f", "g"},
        7: {"a", "c", "f"},
        8: {"a", "b", "c", "d", "e", "f", "g"},
        9: {"a", "b", "c", "d", "f", "g"},
    }
    for k, v in number_to_segments_mapping.items():
        if segments == v:
            return k


def part_a(inputs) -> int:
    outputs = [o for line in inputs for o in line[1]]
    return len([o for o in outputs if len(o) in {2, 3, 4, 7}])


def part_b(inputs) -> int:
    all_output_numbers = []
    for line in inputs:
        mapping = get_mapping(line[0])
        outputs = line[1]
        mapped_outputs = [set(mapping[letter] for letter in output) for output in outputs]
        output_numbers = [match_segments_to_final_number(output) for output in mapped_outputs]
        output_number = int("".join(str(x) for x in output_numbers))
        all_output_numbers.append(output_number)
    return sum(all_output_numbers)


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    print(f"Part A: {part_a(inputs)}")
    print(f"Part B: {part_b(inputs)}")
