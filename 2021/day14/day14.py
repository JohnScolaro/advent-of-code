"""
Problem 14 of the Advent-of-Code 2019
"""
from collections import defaultdict, Counter
from typing import Any, Dict, List, Optional, Set, Tuple
import copy
import more_itertools
from more_itertools.more import windowed


def read_inputs(filename: str) -> List[Any]:
    polymer_template = ""
    pair_insertion_rules = {}
    with open(filename, "r") as fp:
        for line in fp:
            if "->" in line:
                first, second = line.strip().split(" -> ")
                pair_insertion_rules[first] = second
            else:
                if line == "\n":
                    continue
                polymer_template = line.strip()

    return polymer_template, pair_insertion_rules


def step(combos: Dict[str, int], pair_insertion_rules: Dict[str, str]):
    """
    Apply a step to the sets
    """
    new_combos = defaultdict(int)
    for pair in combos:
        if pair in pair_insertion_rules:
            new_combos["".join((pair[0], pair_insertion_rules[pair]))] += combos[pair]
            new_combos["".join((pair_insertion_rules[pair], pair[1]))] += combos[pair]
    return new_combos


def get_combos(polymer_template):
    d = {}
    for x, y in more_itertools.windowed(polymer_template, 2):
        d["".join((x, y))] = d.get("".join((x, y)), 0) + 1
    return d


def part_a(polymer_template, pair_insertion_rules) -> int:
    combos = get_combos(polymer_template)
    for i in range(10):
        combos = step(combos, pair_insertion_rules)
    c = Counter(combos)
    d = defaultdict(int)
    for k, v in c.items():
        a, b = k
        d[a] += v
        d[b] += v
    c = Counter(d)
    c[polymer_template[0]] += 1
    c[polymer_template[-1]] += 1
    return (c.most_common()[0][1] / 2) - (c.most_common()[-1][1] / 2)


def part_b(polymer_template, pair_insertion_rules) -> int:
    combos = get_combos(polymer_template)
    for i in range(40):
        combos = step(combos, pair_insertion_rules)
    c = Counter(combos)
    d = defaultdict(int)
    for k, v in c.items():
        a, b = k
        d[a] += v
        d[b] += v
    c = Counter(d)
    c[polymer_template[0]] += 1
    c[polymer_template[-1]] += 1
    return (c.most_common()[0][1] / 2) - (c.most_common()[-1][1] / 2)


if __name__ == "__main__":
    polymer_template, pair_insertion_rules = read_inputs("input.txt")
    print(f"Part A: {part_a(polymer_template, pair_insertion_rules)}")
    print(f"Part B: {part_b(polymer_template, pair_insertion_rules)}")


# 1088 wrong
# 6461 wrong
# 3231 wrong
# 3230 ...
