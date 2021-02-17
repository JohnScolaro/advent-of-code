"""
Solutions for the Advent of Code - Day 7
"""

class Bag(object):
    def __init__(self, bag_type):
        self.bag_type = bag_type
        self.contains = []

    def add_contains(self, bag, number):
        self.contains.append({'type': bag, 'n': number})


def build_rule_dict(input_file: str) -> dict:
    """
    The data structure I chose to make everything with is the most complicated thing in this function.
    Once that is understood the rest should be simple.

    As I parse each line, I use the bag type as a key, and the associated value is a dictionary:
        This dictionary has a children key whose value is a list of child dictionaries and parent strings.
            Each child dictionary is contains a 'bag_type' key and a 'n' key.
            The parent string is a list of strings of the types of bags that can contain this one.
    """

    bag_dict = {}
    with open(input_file, 'r') as fp:
        for line in fp:
            # String sanitation
            line = line[:-1]
            line = line.replace('.', '').replace(' ', '')
            line = line.replace('bags', '').replace('bag', '')
            bag_type = line.split('contain')[0]

            # Create the bag and put it into the dict.
            bag_dict[bag_type] = {'children': [], 'parents': []}
            # Populate the children list
            contains_list = line.split('contain')[1].split(',')
            for contains in contains_list:
                if contains == 'noother':
                    break
                bag_dict[bag_type]['children'].append({'bag_type': contains[1:], 'n': int(contains[0])})
    
    # Populate the parents list
    for bag in bag_dict:
        for child in bag_dict[bag]['children']:
            bag_dict[child['bag_type']]['parents'].append(bag)

    return bag_dict

def return_all_possible_parents(rule_dict: list, start_bag: str) -> list:
    """ Returns a list of all bags that contain a given other bag """

    # Start by adding the direct parents of the selected bag.
    all_possible_containing_bags = []
    old_len = 0
    all_possible_containing_bags += rule_dict[start_bag]['parents']
    new_len = len(all_possible_containing_bags)

    # Continue adding bags and removing duplicates until no more possible parents are found.
    while (new_len != old_len):
        old_len = new_len
        for bag in all_possible_containing_bags:
            all_possible_containing_bags += rule_dict[bag]['parents']
        all_possible_containing_bags = list(set(all_possible_containing_bags))
        new_len = len(all_possible_containing_bags)

    return all_possible_containing_bags

def total_number_of_contained_bags(rule_dict: list, bag_type: str) -> int:
    """Returns the total number of sub-bags inside a given bag"""
    bag_count = 0

    if rule_dict[bag_type]['children'] == []:
        return 0
    else:
        for child in rule_dict[bag_type]['children']:
            bag_count += total_number_of_contained_bags(rule_dict, child['bag_type']) * child['n'] + child['n']
    
    return bag_count


if __name__ == "__main__":
    rd = build_rule_dict('input.txt')
    
    # Part A
    containing_bags = return_all_possible_parents(rd, 'shinygold')
    print(len(containing_bags))

    # Part B
    total_contained_bags = total_number_of_contained_bags(rd, 'shinygold')
    print(total_contained_bags)
