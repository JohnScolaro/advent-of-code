"""
Solutions for the Advent of Code - Day 23

In this question, Part A asks you to make a circle of cups and to manipulate
the cups according to a few rules. It is hard, and there are a few tricky edge
cases, but it isn't the most difficult problem. In part B, you must simply do
the same thing, but instead of 9 cups, and 100 iterations of the algorithm,
you must do it with 1,000,000 cups and 10,000,000 iterations.

Initially my code for part A took ~2.5 seconds to build the million cup
circle and run 100 iterations. I was storing everything in a list and using
list manipulation and slicing to move the cups around. After lots of thinking
and trying different methods I actually had to consult the internet before
realising the easiest way of implementating the solution to this problem was
to use linked lists. Using linked lists, I can do 100 iterations in less than
a millisecond.
"""

from collections import defaultdict


class Cup():
    def __init__(self):
        self.label = None
        self.next = None


def setup_linked_list(cups: list) -> dict:
    """
    Create a dictionary of cups. The key is the label and the value is the cup.
    """
    d = defaultdict(Cup)
    for i, cup in enumerate(cups):
        next_cup_index = (i + 1) % len(cups)
        d[cup].label = cup
        d[cup].next = d[cups[next_cup_index]]
    d.default_factory = None
    return d


def do_crab_move(cups: dict, selected_cup: int) -> int:
    """
    Manipulate the linked list to do a single crab move.
    """
    picked_up_last_cup = cups[selected_cup].next.next.next
    picked_up_first_cup = cups[selected_cup].next
    picked_up_second_cup = cups[selected_cup].next.next
    picked_up_cups = [picked_up_first_cup.label, picked_up_second_cup.label, picked_up_last_cup.label]
    # Remove picked up cups from the ring
    cups[selected_cup].next = cups[selected_cup].next.next.next.next
    # Calculate destination cup
    destination_cup = selected_cup - 1
    if destination_cup == 0:
        destination_cup = len(cups)
    while destination_cup in picked_up_cups:
        destination_cup -= 1
        if destination_cup == 0:
            destination_cup = len(cups)
    # Add them into the correct location
    picked_up_last_cup.next = cups[destination_cup].next
    cups[destination_cup].next = picked_up_first_cup
    # Return next selected cup
    return cups[selected_cup].next.label


def get_submission_string(cups: dict) -> str:
    """
    This returns the submission string for part A of the coding challenge
    """
    c = cups[1]
    out_str = ''
    for _ in range(len(cups) - 1):
        c = c.next
        out_str += str(c.label)
    return out_str


def part_a() -> list:
    """
    Setup our cups, do 100 iterations of the crab rule, and then print the cups
    in order starting from the cup after 1.
    """
    # Setup cups
    cups = [9, 5, 2, 3, 1, 6, 4, 8, 7]
    current_cup = cups[0]
    cups = setup_linked_list(cups)
    # Run through iterations
    for _ in range(100):
        current_cup = do_crab_move(cups, current_cup)
    # Return answer
    return get_submission_string(cups)


def part_b():
    """
    Setup our million cups, do 10 million iterations of the crab rule, then get
    the two cups clockwise of cup 1, multiply them together and return that
    number for submission.
    """
    # Setup cups
    cups = [9, 5, 2, 3, 1, 6, 4, 8, 7]
    current_cup = cups[0]
    for x in range(10, 1000001):
        cups.append(x)
    cups = setup_linked_list(cups)
    # Run through iterations
    for _ in range(10000000):
        current_cup = do_crab_move(cups, current_cup)
    # Return answer
    return cups[1].next.label * cups[1].next.next.label


if __name__ == "__main__":
    print("Part A: " + part_a())
    print("Part B: " + str(part_b()))
