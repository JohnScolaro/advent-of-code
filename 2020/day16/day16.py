"""
Solutions for the Advent of Code - Day 16
"""


class Field(object):
    """
    An object representing a train ticket field and rules that the numbers on
    the card must follow.
    """
    def __init__(self, name: str, range1: str, range2: str):
        self.range1 = range1.split('-')
        self.range1 = (int(self.range1[0]), int(self.range1[1]))
        self.range2 = range2.split('-')
        self.range2 = (int(self.range2[0]), int(self.range2[1]))
        self.name = name

    def in_range(self, n: int):
        if self.range1[0] <= n <= self.range1[1]:
            return True
        if self.range2[0] <= n <= self.range2[1]:
            return True
        return False


def read_input(file_name: str):
    """
    String parsing. Going to be fairly ugly no matter how you do it.
    """
    lines = []
    with open(file_name, 'r') as fb:
        for line in fb:
            lines.append(line.strip())

    fields = lines[0:20]
    fields = [line.replace(' or ', ':').replace(' ', '').split(':') for line in fields]
    fields = [Field(x[0], x[1], x[2]) for x in fields]
    our_ticket = [int(x) for x in lines[22].split(',')]
    nearby_tickets = [x.split(',') for x in lines[25:]]
    nearby_tickets = [[int(value) for value in line] for line in nearby_tickets]
    return (fields, our_ticket, nearby_tickets)


def get_valid_numbers(fields: list):
    """
    Takes a list of fields objects, and creates a set of numbers that
    are valid.
    """
    s = set()
    for f in fields:
        for x in range(f.range1[0], f.range1[1] + 1):
            s.add(x)
        for x in range(f.range2[0], f.range2[1] + 1):
            s.add(x)
    return s


def part_a(fields: list, nearby_tickets: list):
    """
    Find the sum of all values on all tickets that are not valid in any field.
    """
    set_of_valid_numbers = get_valid_numbers(fields)

    sum_of_invalid_nums = 0
    for ticket in nearby_tickets:
        for value in ticket:
            if value not in set_of_valid_numbers:
                sum_of_invalid_nums += value

    return sum_of_invalid_nums


def is_ticket_valid(ticket: list, valid_numbers: set):
    for field in ticket:
        if field not in valid_numbers:
            return False
    return True


def all_sets_are_single_element(sets: list) -> bool:
    for x in sets:
        if len(x) != 1:
            return False
    return True


def get_cols(fields: list, tickets: list):
    """
    The crux of this algorithm is to create a set of all the columns that could
    possible still satisfy each rule. These sets all start with all the columns
    in them, but as we check every element of every row to see if they match
    every rule, if they fail the rule, we remove that column from possibly
    satisfying that field. At the of the algorithm we are left with only a few
    possibilities for each set. We can then use deduction (if col 16 must be
    departure date, then col 17 can't be departure date, etc) to figure out
    which columns must be each field.
    """

    # Initialise sets with all the numbers
    col_sets = [set() for x in range(len(fields))]
    for col_set in col_sets:
        for i in range(len(fields)):
            col_set.add(i)

    # Check every value of every ticket against every field.
    for tickets in valid_tickets:
        for ticket_i, ticket_value in enumerate(tickets):
            for field_i, field in enumerate(fields):
                if not field.in_range(ticket_value):
                    col_sets[field_i].discard(ticket_i)

    # Using deduction to determine the only possible valid columns.
    numbers_determined = set()
    while not all_sets_are_single_element(col_sets):
        for s in col_sets:
            if len(s) > 1:
                for n in numbers_determined:
                    s.discard(n)
            if len(s) == 1:
                numbers_determined.add(list(s)[0])

    return [list(x)[0] for x in col_sets]


def part_b(fields: list, our_ticket: list, valid_tickets: list):
    cols = get_cols(fields, valid_tickets)

    # Figure out what fields we want to read.
    departure_fields = set()
    for i, field in enumerate(fields):
        if field.name.startswith('departure'):
            departure_fields.add(i)

    prod = 1
    for departure_field in departure_fields:
        prod *= our_ticket[cols[departure_field]]
    return prod


if __name__ == "__main__":
    fields, our_ticket, nearby_tickets = read_input('input.txt')
    print("Part A: " + str(part_a(fields, nearby_tickets)))
    valid_tickets = [ticket for ticket in nearby_tickets if is_ticket_valid(ticket, get_valid_numbers(fields))]
    print("Part B: " + str(part_b(fields, our_ticket, valid_tickets)))
