"""
Solutions for the Advent of Code - Day 11

If I was coding up a more general solution, I'd make the 'find number of
people around you sitting' function some hot-swappable function call, but
since it's just a coding challenge, I'm not, and this appears a little hacky.
"""


def get_layout(filename: str) -> list:
    layout = []
    with open(filename, 'r') as fb:
        for line in fb:
            layout.append(line[:-1])
    return layout


def one_iteration(old_layout: list, part_a: bool) -> list:
    """ Takes the old layout, returns the new layout """
    new_layout = old_layout[:]
    for x in range(len(old_layout[0])):
        for y in range(len(old_layout)):
            if old_layout[y][x] == 'L':
                if num_adjacent_occupied_seats(old_layout, (x, y), part_a) == 0:
                    new_layout[y] = new_layout[y][:x] + '#' + new_layout[y][x+1:]
            elif old_layout[y][x] == '#':
                if num_adjacent_occupied_seats(old_layout, (x, y), part_a) >= (4 if part_a else 5):
                    new_layout[y] = new_layout[y][:x] + 'L' + new_layout[y][x+1:]

    return new_layout


def num_adjacent_occupied_seats(layout: list, position: tuple, part_a: bool) -> list:
    if part_a:
        return is_seat_occupied(layout, (position[0] - 1, position[1] - 1)) + \
            is_seat_occupied(layout, (position[0] - 1, position[1])) + \
            is_seat_occupied(layout, (position[0] - 1, position[1] + 1)) + \
            is_seat_occupied(layout, (position[0], position[1] - 1)) + \
            is_seat_occupied(layout, (position[0], position[1] + 1)) + \
            is_seat_occupied(layout, (position[0] + 1, position[1] - 1)) + \
            is_seat_occupied(layout, (position[0] + 1, position[1])) + \
            is_seat_occupied(layout, (position[0] + 1, position[1] + 1))
    else:
        return is_seat_occupied_in_direction(layout, position, (0, 1)) + \
            is_seat_occupied_in_direction(layout, position, (1, 1)) + \
            is_seat_occupied_in_direction(layout, position, (1, 0)) + \
            is_seat_occupied_in_direction(layout, position, (0, -1)) + \
            is_seat_occupied_in_direction(layout, position, (-1, -1)) + \
            is_seat_occupied_in_direction(layout, position, (-1, 0)) + \
            is_seat_occupied_in_direction(layout, position, (-1, 1)) + \
            is_seat_occupied_in_direction(layout, position, (1, -1))


def is_seat_occupied(layout: list, position: tuple) -> int:
    """ Returns 1 if seat occupied, otherwise 0 """
    max_x = len(layout[0])
    max_y = len(layout)
    if position[0] < 0 or position[1] < 0:
        return 0
    if position[0] >= max_x or position[1] >= max_y:
        return 0
    if layout[position[1]][position[0]] == '#':
        return 1
    else:
        return 0


def is_seat_occupied_in_direction(layout: list, position: tuple, direction: tuple) -> int:
    """ Returns 1 if seat occupied, otherwise 0 """
    max_x = len(layout[0])
    max_y = len(layout)

    # Apply one step away from initial position before starting to loop
    position = (position[0] + direction[0], position[1] + direction[1])

    while True:
        if position[0] < 0 or position[1] < 0:
            return 0
        if position[0] >= max_x or position[1] >= max_y:
            return 0
        if layout[position[1]][position[0]] == '#':
            return 1
        if layout[position[1]][position[0]] == 'L':
            return 0
        position = (position[0] + direction[0], position[1] + direction[1])


def layouts_equal(old_layout: list, new_layout: list) -> bool:
    """ Tests to see if two layouts are equal or not """
    for i in range(len(old_layout)):
        if old_layout[i] != new_layout[i]:
            return False
    return True


def number_of_occupied_seats(layout: list) -> int:
    """ Returns the number of occupied seats in a layout """
    count = 0
    for x in layout:
        count += x.count('#')
    return count


def num_occupied_seats_at_stable_solution(layout: list, part_a: bool) -> int:
    """
    Runs a simulation over a number of iterations until a stable solution is
    found. Once this happens, then we return the number of occupied seats.

    Part a is true = Part A's solution.
    Part a is false = Part B's solution
    """
    old_layout = layout
    new_layout = one_iteration(old_layout, part_a)
    i = 0
    while True:
        if layouts_equal(old_layout, new_layout):
            return number_of_occupied_seats(new_layout)
        else:
            old_layout = new_layout
            new_layout = one_iteration(old_layout, part_a)
        i += 1


if __name__ == "__main__":
    layout = get_layout('input.txt')
    print("Part A: " + str(num_occupied_seats_at_stable_solution(layout, True)))
    print("Part B: " + str(num_occupied_seats_at_stable_solution(layout, False)))
