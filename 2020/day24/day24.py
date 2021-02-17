"""
Solutions for the Advent of Code - Day 24
"""

from collections import Counter

def read_input(file_name: str):
    """
    Reads inputs into a bunch of strings. The 6 commands are turned into
    numbers because that'll be far easier to deal with later.
    """
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            line = line.replace('se', '2')
            line = line.replace('sw', '3')
            line = line.replace('ne', '6')
            line = line.replace('nw', '5')
            line = line.replace('w', '4')
            line = line.replace('e', '1')
            l.append(line.strip())
    return l

def get_coord(instructions: str):
    """
    Get final coordinate of a tile from the starting tile from a list of
    instructions.
    """
    x = 0
    y = 0
    for instruction in instructions:
        if instruction == '1': # E
            x += 1
        elif instruction == '2': # SE
            if (y % 2 == 1):
                x += 1
            y -= 1
        elif instruction == '3': # SW
            if (y % 2 == 0):
                x -= 1
            y -= 1
        elif instruction == '4': # W
            x -= 1
        elif instruction == '5': # NW
            if (y % 2 == 0):
                x -= 1
            y += 1
        elif instruction == '6': # NE
            if (y % 2 == 1):
                x += 1
            y += 1
    return (x, y)

def get_all_tile_flips(list_of_instruction_lists: list) -> Counter:
    """ Get counter counting each time that a tile is flipped. """
    c = Counter()
    for instruction_list in list_of_instruction_lists:
        c[get_coord(instruction_list)] += 1
    return c

def part_a(list_of_instruction_lists: list) -> int:
    """ Return the total number of black tiles """
    c = get_all_tile_flips(list_of_instruction_lists)
    s = 0
    for x in c.values():
        if x % 2 != 0:
            s += 1
    return s

def get_neighbours(tile: tuple) -> set:
    """ Returns a set of all tiles neighbouring the input tile. """
    x = tile[0]
    y = tile[1]
    s = set([(x-1, y), (x+1, y)])
    if (y % 2 == 0):
        return s.union({(x, y+1), (x-1, y+1), (x, y-1), (x-1, y-1)})
    else:
        return s.union({(x+1, y+1), (x, y+1), (x+1, y-1), (x, y-1)})

def day_iteration(black_tiles: set) -> set:
    """
    Carrys out the tiles changes that occur between days for part B by
    returning a new set of black tiles.
    """
    new_black_tiles = set()

    # Add black tiles that remain black
    for black_tile in black_tiles:
        if 0 < len(get_neighbours(black_tile).intersection(black_tiles)) < 3:
            new_black_tiles.add(black_tile)

    # Get all neighbours
    neighbours = set()
    for black_tile in black_tiles:
        neighbours = neighbours.union(get_neighbours(black_tile))
    neighbours = neighbours.difference(black_tiles)

    # Add white tiles that turn black
    for neighbour in neighbours:
        if len(get_neighbours(neighbour).intersection(black_tiles)) == 2:
            new_black_tiles.add(neighbour)

    return new_black_tiles

def part_b(list_of_instruction_lists: list) -> int:
    # Get set of black tiles
    c = get_all_tile_flips(list_of_instruction_lists)
    black_tiles = set()
    for k, v in c.items():
        if (v % 2) != 0:
            black_tiles.add(k)

    # Carry out a number of iterations
    for _ in range(100):
        black_tiles = day_iteration(black_tiles)

    return len(black_tiles)

if __name__ == "__main__":
    l = read_input('input.txt')
    print("Part A: " + str(part_a(l)))
    print("Part B: " + str(part_b(l)))
