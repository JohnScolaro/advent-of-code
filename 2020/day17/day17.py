"""
Solutions for the Advent of Code - Day 17

I starting using custom point objects to solve this, but thought that most of
the logic in this solution could be simplified by simply using sets. To do this
we need to use immutable objects to store in the sets, so I'm using three
tuples instead.
"""

import itertools


def get_starting_active_points(input_file: str, dims: int) -> set:
    """ Takes input file and returns a set of active points """
    s = set()
    with open(input_file, 'r') as fb:
        for y, line in enumerate(fb):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    tmp_list = [x, y]
                    for _ in range(dims-2):
                        tmp_list.append(0)
                    s.add(tuple(tmp_list))
    return s


def get_neighbours(point: tuple) -> set:
    """ Takes a point and returns a set of all neighbours """
    lists = [list() for _ in range(len(point))]
    for i, n in enumerate(point):
        lists[i].append(n - 1)
        lists[i].append(n)
        lists[i].append(n + 1)
    s = set(itertools.product(*lists))
    s.remove(point)
    return s


def tick_in_game_time(active_points: set) -> set:
    """
    Takes a set of active points, performs a single tick of game time and
    returns the list of active points after the single tick.
    """
    future_active_points = set()

    # First, check to see which of the currently active points will stay active.
    for point in active_points:
        neighbors = get_neighbours(point)
        active_neighbours = neighbors.intersection(active_points)
        if 2 <= len(active_neighbours) <= 3:
            future_active_points.add(point)

    # Next, check which other points will turn on. (Only worth checking neighbors).
    neighbors_to_check = set()
    for point in active_points:
        neighbors_to_check = neighbors_to_check.union(get_neighbours(point))
    for neighbor in neighbors_to_check:
        neighbor_neighbours = get_neighbours(neighbor)
        active_neighbours = neighbor_neighbours.intersection(active_points)
        if len(active_neighbours) == 3:
            future_active_points.add(neighbor)

    return future_active_points


def execute_n_ticks(active_points: set, n) -> set:
    """ Execute n ticks in game time """
    for _ in range(n):
        active_points = tick_in_game_time(active_points)
    return active_points


if __name__ == "__main__":
    print("Part A: " + str(len(execute_n_ticks(get_starting_active_points('input.txt', 3), 6))))
    print("Part B: " + str(len(execute_n_ticks(get_starting_active_points('input.txt', 4), 6))))
