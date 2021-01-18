'''
Solutions for the Advent of Code - Day 12
'''

class PartAShip(object):
    def __init__(self, current_heading: str):
        self.current_heading = current_heading
        self.total_movement_north = 0
        self.total_movement_east = 0

    def _rotate(self, direction: str, degrees: int):
        if direction == 'R':
            right_rotation = degrees
        else:
            right_rotation = 360 - degrees

        index_rotation = right_rotation//90
        current_index = 'NESW'.find(self.current_heading)
        current_index = (current_index + index_rotation) % 4
        self.current_heading = 'NESW'[current_index]

    def handle_instruction(self, command: str, value: int):
        if command == 'N':
            self.total_movement_north += value
        if command == 'S':
            self.total_movement_north -= value
        if command == 'E':
            self.total_movement_east += value
        if command == 'W':
            self.total_movement_east -= value
        if command == 'L':
            self._rotate('L', value)
        if command == 'R':
            self._rotate('R', value)
        if command == 'F':
            self.handle_instruction(self.current_heading, value)

class PartBShip(object):
    def __init__(self, waypoint_relative_loc: tuple):
        self.waypoint_north = waypoint_relative_loc[0]
        self.waypoint_east = waypoint_relative_loc[1]
        self.total_movement_north = 0
        self.total_movement_east = 0

    def _rotate(self, direction: str, degrees: int):
        # Determine how many times we are going to turn right.
        if direction == 'R':
            right_rotation = degrees
        else:
            right_rotation = 360 - degrees
        right_rotation = right_rotation//90

        # Carry out rotations
        while right_rotation != 0:
            wpe = self.waypoint_east
            wpn = self.waypoint_north
            self.waypoint_east = wpn
            self.waypoint_north = -wpe
            right_rotation -= 1

    def handle_instruction(self, command: str, value: int):
        if command == 'N':
            self.waypoint_north += value
        if command == 'S':
            self.waypoint_north -= value
        if command == 'E':
            self.waypoint_east += value
        if command == 'W':
            self.waypoint_east -= value
        if command == 'L':
            self._rotate('L', value)
        if command == 'R':
            self._rotate('R', value)
        if command == 'F':
            self.total_movement_north += self.waypoint_north * value
            self.total_movement_east += self.waypoint_east * value
        
def parse_instruction(instruction: str) -> tuple:
    command = instruction[0]
    value = int(instruction[1:])
    return (command, value)

def get_navigation_instructions(input_file: str) -> list:
    nav_inst = []
    with open(input_file, 'r') as fb:
        for line in fb:
            nav_inst.append(line[:-1])
    return nav_inst

def run_ship_through_all_instructions(list_of_instructions: list, ship):
    for instruction in navigation_instructions:
        command, value = parse_instruction(instruction)
        ship.handle_instruction(command, value)
    return abs(ship.total_movement_east) + abs(ship.total_movement_north)


if __name__ == "__main__":
    navigation_instructions = get_navigation_instructions('input.txt')
    
    # Part A
    a_ship = PartAShip('E')
    print("Part A: " + str(run_ship_through_all_instructions(navigation_instructions, a_ship)))

    # Part B
    b_ship = PartBShip((1, 10))
    print("Part B: " + str(run_ship_through_all_instructions(navigation_instructions, b_ship)))
    