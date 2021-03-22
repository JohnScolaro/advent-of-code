"""
Problem 6 of the Advent-of-Code 2019

We are orbitting a planet, orbitting a planet, orbitting a planet, etc.
If nothing else, this question made me google the name of the planet that is
being orbitted by another planet. If a moon is orbitting a planet, the
celestial body that it is orbitting is called that moon's 'primary'.
"""

class Planet():
    """
    Moon objects contain a small amount of information about their state.
    Specifically their direct primary, all indirect primaries, and their list
    of moons.
    """

    def __init__(self):
        self.primary = None
        self.moons = []
        self.primaries = []

    def add_indirect_primaries(self, planets: dict) -> None:
        """
        A function that adds all primaries of this planet to its moons. Then
        calls the same function on all its moons. This lets us simply call this
        function once on the 'COM' node and then the indirect primaries for all
        planets are calculated.
        """
        for moon in self.moons:
            planets[moon].primaries = planets[moon].primaries + self.primaries
            planets[moon].add_indirect_primaries(planets)


def read_inputs(filename: str) -> dict:
    """
    From the input file, return a dictionary of Planets. The keys are the names
    of the planets, and the values are the planets themself.
    """
    planets = {}
    inputs = []

    # Read data into initial temp list.
    with open(filename, 'r') as fp:
        for line in fp:
            primary, secondary = line.strip().split(')')
            inputs.append((primary, secondary))
    
    # Add COM first, then add all planets.
    planets['COM'] = Planet()
    for i in inputs:
        planets[i[1]] = Planet()

    # Now that all planets exist, lets populate their information.
    for i in inputs:
        planets[i[1]].primaries.append(i[0])
        planets[i[1]].primary = i[0]
        planets[i[0]].moons.append(i[1])

    # Filling in all the indirect primaries of the moons.
    planets['COM'].add_indirect_primaries(planets)
    return planets

def get_list_of_decendants(planets: dict, planet: str) -> list:
    """
    Returns a list of planets that are all direct primaries of eachother.

    Args:
        planets (dict): A dictionary of all planets in the solar system.
        planet (str): The name of the planet we want to get the decendants of.

    Example Returns:
        ['COM', 'ABC', '123', 'JON']

    In this example, we would have asked for the decendances of 'JON' and it
    returns the primaries of 'JON' all the way back to the 'COM'.
    """
    decendants = []
    p = planet
    while p != 'COM':
        decendants.append(p)
        p = planets[p].primary
    decendants.append('COM')
    return decendants

def part_a(planets: dict) -> int:
    """
    Solves part A. Adds together all the direct and indirect primaries of all
    the planets in the solar system.
    """
    return sum([len(planet.primaries) for planet in planets.values()])
    
def part_b(planets: dict) -> int:
    """
    Finds the total number of orbital transfers needed for YOU to get to SAN.
    """
    # Get both planets list of decendants.
    santa_deps = get_list_of_decendants(planets, 'SAN')
    you_deps = get_list_of_decendants(planets, 'YOU')

    # Using the fact that some part of both strings will be the same before
    # inevitably reaching COM, we can pop off the similar ending elements,
    # returning only the unique paths.
    while santa_deps[-1] == you_deps[-1]:
        santa_deps.pop()
        you_deps.pop()
    
    # The number of orbital transfers needed between SAN and the common node is
    # len(decendants) - 1. Same for the YOU node.
    return len(santa_deps) + len(you_deps) - 2


if __name__ == "__main__":
    l = read_inputs('input.txt')
    print("Part A: {}".format(str(part_a(l))))
    print("Part B: {}".format(str(part_b(l))))
