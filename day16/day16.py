'''
Solutions for the Advent of Code - Day 16
'''

import numpy as np

class Field(object):
    def __init__(self, name: str, range1: str, range2: str):
        self.range1 = range1.split('-')
        self.range1 = (int(self.range1[0]), int(self.range1[1]))
        self.range2 = range2.split('-')
        self.range2 = (int(self.range2[0]), int(self.range2[1]))
        self.name = name

def read_input(file_name: str):
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            l.append(line.strip())

    fields = l[0:20]
    fields = [line.replace(' or ', ':').replace(' ', '').split(':') for line in fields]
    fields = [Field(x[0], x[1], x[2]) for x in fields]
    our_ticket = [int(x) for x in l[22].split(',')]
    nearby_tickets = [x.split(',') for x in l[25:]]
    nearby_tickets = [[int(value) for value in line] for line in nearby_tickets]
    return (fields, our_ticket, nearby_tickets)

def get_valid_numbers(fields: list):
    '''
    Takes a list of fields of value numbers, and creates a set of numbers that
    are valid.
    '''
    s = set()
    for r in fields:
        for x in range(r[0], r[1] + 1):
            s.add(x)
    return s

def part_a(fields, nearby_tickets):
    '''
    Find the sum of all values on all tickets that are not valid in any field.
    '''
    f = []
    for field in fields:
        f.append(field.range1)
        f.append(field.range2)
    set_of_valid_numbers = get_valid_numbers(f)

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

def get_ranges_of_fields(nearby_tickets: list):
    tickets = np.array(nearby_tickets)
    print(np.shape(tickets))
    tickets = np.transpose(tickets)
    print(np.shape(tickets))
    maxs = np.max(tickets)
    mins = np.min(tickets)
    print(np.shape(mins))

    return list(zip(mins, maxs))
    
if __name__ == "__main__":
    fields, our_ticket, nearby_tickets = read_input('input.txt')
    print("Part A: " + str(part_a(fields, nearby_tickets)))
    valid_tickets = [ticket for ticket in nearby_tickets if is_ticket_valid(ticket)]
    field_ranges = get_ranges_of_fields(valid_tickets)
    print(field_ranges)