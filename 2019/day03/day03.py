"""
Problem 3 of the Advent-of-Code 2019
"""

def read_inputs(filename: str):
    l = []
    with open(filename, 'r') as fp:
        for line in fp:
            l.append(line.strip())
    return l

def get_instructions_from_string(string_of_instructions: str) -> list:
    """
    Returns a list of tuples like so: ('U', 3)
    """
    return [(x[0], int(x[1:])) for x in string_of_instructions.split(',')]

def get_all_coords_with_wire_on_them(list_of_instructions: list) -> set:
    """
    It is easy to find crossings if we just simply have sets of all the
    coordinates the wire exists at. Then we can simply find the points that
    exist in multiple sets. This function returns a set of all the coordinates
    this wire exists at if we follow the instructions from the origin point.
    """
    wire_positions = set()
    loc = (0, 0)
    for instruction in list_of_instructions:
        direction = instruction[0]
        distance = instruction[1]
        if direction == 'U':
            increment = (0, 1)
        elif direction == 'L':
            increment = (-1, 0)
        elif direction == 'R':
            increment = (1, 0)
        elif direction == 'D':
            increment = (0, -1)
        for i in range(distance):
            wire_positions.add((loc[0] + (i * increment[0]), loc[1] + (i * increment[1])))
        loc = (loc[0] + (distance * increment[0]), loc[1] + (distance * increment[1]))
    wire_positions.add(loc)
    return wire_positions

def steps_to_get_to_point(list_of_instructions: list, point: tuple) -> int:
    """
    
    """
    pass


def part_a(wire_paths: list):
    """
    Find all the crossings, then return the manhattan distance of the crossing
    with the smallest manhattan distance to the origin point.
    """
    wire_1_locs = get_all_coords_with_wire_on_them(get_instructions_from_string(wire_paths[0]))
    wire_2_locs = get_all_coords_with_wire_on_them(get_instructions_from_string(wire_paths[1]))
    crossings = wire_1_locs.intersection(wire_2_locs)
    crossings.remove((0, 0)) # Remove origin point
    crossings = list(crossings)
    m_distances = [abs(x[0]) + abs(x[1]) for x in crossings]
    min_crossing = crossings[m_distances.index(min(m_distances))]
    return (abs(min_crossing[0]) + abs(min_crossing[1]))
    
def part_b(wire_paths: list):
    """
    """
    pass

if __name__ == "__main__":
    l = read_inputs('input.txt')
    print("Part A: " + str(part_a(l)))
    print("Part B: " + str(part_b(l)))
