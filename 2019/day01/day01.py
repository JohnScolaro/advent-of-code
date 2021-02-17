"""
Problem 1 of the Advent-of-Code 2019
"""

def read_inputs(filename: str) -> list:
    """ Read module weights in as a list of ints """
    l = []
    with open(filename, 'r') as fp:
        for line in fp:
            l.append(int(line.strip()))
    return l

def part_a(module_weights: int) -> int:
    """ Calculate weight of fuel needed for each module and add together """
    sum_of_fuel = 0
    for module_weight in module_weights:
        sum_of_fuel += ((module_weight // 3) - 2)
    return sum_of_fuel

def part_b(module_weights: int) -> int:
    """
    Calculate weight of fuel needed for each module, then the fuel needed for
    that fuel, and the fuel needed for that fuel... etc, until no more fuel is
    needed. Calculate the sum of these.
    """
    sum_of_fuel = 0
    for module_weight in module_weights:
        total_fuel_for_this_module = ((module_weight // 3) - 2)
        additional_fuel = ((module_weight // 3) - 2)
        while True:
            additional_fuel = ((additional_fuel // 3) - 2)
            if additional_fuel <= 0:
                break
            else:
                total_fuel_for_this_module += additional_fuel
        sum_of_fuel += total_fuel_for_this_module
    return sum_of_fuel

if __name__ == "__main__":
    l = read_inputs('input.txt')
    print("Part A: " + str(part_a(l)))
    print("Part B: " + str(part_b(l)))