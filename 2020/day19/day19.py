"""
Solutions for the Advent of Code - Day 19

My solution may differ from others you'll see online because, for one, I don't
use regex. I do this for 2 reasons. 1: I suck at regex. 2: I implemented my
solution before I looked online and saw everyone else was using regex.

Part A:
For part A, I recursively traverse the rules, starting from rule 0, calling
the 'generate_matching_string' function on all sub rules until finally a set
containing all valid strings is returned. For every message, we simply check
if it is in the set or not. Relatively simple.

Part B:
Part B, is much harder. I started by attempting to simply limit the depth of
recusion to some artificial limit. This would work given infinite computational
power, but since we would need to generate all strings up to 80 chars long,
(and since each of rule 42 and 31 yield sets of strings with only 8 chars)
that's over len(set_of_all_matching_strings(42)) ^ 8 variations to store in
memory. Simply not feasable.

The big breakthrough comes with the combination of 2 findings:
    1: The set of matching strings for rule 31 and rule 42 are all 8 char
        length strings.
    2: The 0 rule immediately calls rule 8 and 11 which immediately loop.
        Since Rule 8 can be any number of 42's, and rule 11 can be n * Rule
        42's followed by n * rule 31's where n is a positive real number. This
        means that for a target string of length x * 8, it must consist of
        at least 8/2 + 1 chunks from the set of Rule 42, and at least 1 chunk
        of Rule 31 at the end. The chunks can change from being Rule 42 to Rule
        31 at any point after half way.

When these logically clicked in my head, I figured I'd just calculate part B
in a different way. I'd chunk the target string into 8's and see if each of the
chunks are in the corresponding sets of Rules 42 and 31 according to dot point
2 above.
"""

import itertools

class Rule(object):
    def __init__(self, rule_num: int, rule: str):
        self.rule_num = rule_num
        self.rule = rule

    def generate_matching_string(self, rule_set: dict) -> set:
        """
        Takes a set of all tules and returns the possible matching sets of
        strings for the rule it is called on.
        """
        s = set()
        # If it's an 'or' rule
        if '|' in self.rule:
            for rule in self.rule.split(' | '):
                s = s | self.joining_rule(rule, rule_set)
        # If it's a single letter rule
        elif '"' in self.rule:
            s.add(self.rule.replace('"', ''))
        # If it's a joining rule
        else:
            s = s | self.joining_rule(self.rule, rule_set)

        return s

    def joining_rule(self, rule: str, rule_set: dict) -> set:
        """
        Takes a string in the format of two numbers seperated by a space.
        Returns the set of possible matches for the combination of those rules.
        """
        s = set()
        if " " in rule:
            l = []
            for individual_match in rule.split(" "):
                if (int(individual_match) == self.rule_num): # Congrats we have a loop
                    continue
                matches = rule_set[int(individual_match)].generate_matching_string(rule_set)
                l.append(matches)
            s = s | set([''.join(x) for x in itertools.product(*l)])
        else:
            # Single rule
            s = s | rule_set[int(rule)].generate_matching_string(rule_set)
        return s

def read_input(file_name: str):
    """ Reads input into list of rule lines and list of message lines """
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            l.append(line.strip())
    return (l[:135], l[136:])

def rule_parser(rules: list) -> dict:
    """ Takes a list of rule strings, and returns a set of list objects """
    r = {}
    for rule in rules:
        r[int(rule.split(':')[0])] = Rule(int(rule.split(':')[0]), rule.split(':')[1][1:])
    return r

def number_of_matches_part_a(matches: set, messages: list, rule_set: dict) -> int:
    """
    Takes a set of matching strings and a list of messages and returns the
    number of messages with metching strings in them.
    """
    s = 0
    for message in messages:
        # Check if the message is simply in the matches
        if message in matches:
            s += 1
    return s

def number_of_matches_part_b(messages: list, rule_set: dict) -> bool:
    """
    We use a different method of counting matches for part B.
    """
    s = 0
    for message in messages:
        message_decomp = [(message[i:i+8]) for i in range(0, len(message), 8)] 
        l = []
        l.append(rule_set[42].generate_matching_string(rule_set))
        l.append(rule_set[31].generate_matching_string(rule_set))
        m_flag = True
        n = 0
        for i, m in enumerate(message_decomp):
            if m not in l[n]:
                if i <= len(message_decomp) / 2: # If we switch to rule 31 before or at half way
                    m_flag = False
                    break
                if n == 1: # If Rule 31 doesn't work
                    m_flag = False
                    break
                if m not in l[n+1]:
                    m_flag = False
                    break
                else:
                    n += 1
        if m_flag:
            if n == 1:
                s += 1
    return s


if __name__ == "__main__":
    rules, messages = read_input('input_part_a.txt')
    rules = rule_parser(rules)

    matches = rules[0].generate_matching_string(rules)
    print("Part A: " + str(number_of_matches_part_a(matches, messages, rules)))

    rules, messages = read_input('input_part_b.txt')
    rules = rule_parser(rules)

    print("Part B: " + str(number_of_matches_part_b(messages, rules)))
