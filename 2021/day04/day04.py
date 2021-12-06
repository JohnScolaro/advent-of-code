"""
Problem 4 of the Advent-of-Code 2021
"""

from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    input = []
    with open(filename, "r") as fp:
        for line in fp:
            input.append(line.strip())
    return input


def part_a(numbers_called, bingo_cards):
    called_numbers = set()
    for number in numbers_called:
        called_numbers.add(number)
        for card in bingo_cards:
            if is_card_complete(card, called_numbers):
                return number * get_sum_of_unmarked_numbers(card, called_numbers)


def part_b(numbers_called, bingo_cards):
    called_numbers = set()
    finished_card_indexes = set()

    for number in numbers_called:
        called_numbers.add(number)

        # If one left
        if len(finished_card_indexes) == len(bingo_cards) - 1:
            (last_card_index,) = set(i for i in range(len(bingo_cards)) if i not in finished_card_indexes)
            return number * get_sum_of_unmarked_numbers(bingo_cards[last_card_index], called_numbers)

        # Otherwise
        for i in range(len(bingo_cards)):
            if i not in finished_card_indexes:
                if is_card_complete(bingo_cards[i], called_numbers):
                    finished_card_indexes.add(i)

    return 0


def get_sum_of_unmarked_numbers(card, called_numbers) -> int:
    return sum(cell for row in card for cell in row if cell not in called_numbers)


def is_card_complete(card, called_numbers: set) -> bool:
    for row in card:
        if all(cell in called_numbers for cell in row):
            return True
    for i in range(len(card[0])):
        if all(row[i] in called_numbers for row in card):
            return True
    return False


def get_numbers_called(inputs):
    return [int(x) for x in inputs[0].split(",")]


def get_bingo_cards(inputs):
    bingo_cards = []
    card = []
    for line in inputs[2:]:
        if line != "":
            card.append([int(x) for x in line.split()])
        else:
            bingo_cards.append(card)
            card = []
    return bingo_cards


if __name__ == "__main__":
    inputs = read_inputs("input.txt")
    numbers_called = get_numbers_called(inputs)
    bingo_cards = get_bingo_cards(inputs)

    # print(input)
    print(f"Part A: {part_a(numbers_called, bingo_cards)}")
    print(f"Part B: {part_b(numbers_called, bingo_cards)}")
