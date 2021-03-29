"""
Solutions for the Advent of Code - Day 3
Tuples are all in the format (x, y) where x is horizontal distance increasing
to the right, and y is the vertical distance increasing as you go down the
slope.
"""

from typing import List, Tuple

Coordinate = Tuple[int, int]


def is_position_a_tree(ski_slope: List[str], position: Coordinate) -> bool:
    """
    Given a ski slope and a coordinate, returns whether or not that coordinate
    is a tree.
    """
    return ski_slope[position[1]][position[0]] == '#'


def change_position(ski_slope: List[str], cur_coords: Coordinate, requested_move: Coordinate) -> Coordinate:
    width_of_slope = len(ski_slope[0])
    new_position = ((cur_coords[0] + requested_move[0]) % (width_of_slope - 1), cur_coords[1] + requested_move[1])
    return new_position


def are_we_at_the_bottom(ski_slope: List[str], current_position: Coordinate) -> bool:
    return current_position[1] == len(ski_slope) - 1


def trees_encountered_on_descent(ski_slope: List[str], movement: Coordinate) -> int:
    num_trees = 0
    current_position = (0, 0)

    while not are_we_at_the_bottom(ski_slope, current_position):
        current_position = change_position(ski_slope, current_position, movement)
        if is_position_a_tree(ski_slope, current_position):
            num_trees += 1
    return num_trees


if __name__ == "__main__":
    # Read whole file in as a list of strings.
    ski_slope = []
    with open('input.txt', 'r') as fp:
        for line in fp:
            ski_slope.append(line)

    trees = []
    trees.append(trees_encountered_on_descent(ski_slope, (1, 1)))
    trees.append(trees_encountered_on_descent(ski_slope, (3, 1)))
    trees.append(trees_encountered_on_descent(ski_slope, (5, 1)))
    trees.append(trees_encountered_on_descent(ski_slope, (7, 1)))
    trees.append(trees_encountered_on_descent(ski_slope, (1, 2)))

    product = 1
    for x in trees:
        product *= x

    print(product)
