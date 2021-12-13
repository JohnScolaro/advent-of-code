"""
Problem 12 of the Advent-of-Code 2019
"""
from typing import Any, Dict, List, Optional, Set, Tuple
import copy


class Cave:
    def __init__(self, name: str, large: bool):
        self.name = name
        self.connected_caves = []
        self.large = large

    def is_large(self) -> bool:
        return self.large

    def append_connected_caves(self, connected_caves: List[str]) -> None:
        self.connected_caves.extend(connected_caves)

    def __repr__(self):
        return f"{self.name}: connected to {','.join(self.connected_caves)}"


def read_inputs(filename: str) -> List[Any]:
    lines = []
    with open(filename, "r") as fp:
        for line in fp:
            lines.append(line)

    caves = {}
    for line in lines:
        cave_a, cave_b = line.strip().split("-")
        caves[cave_a] = Cave(cave_a, cave_a.isupper())
        caves[cave_b] = Cave(cave_b, cave_b.isupper())

    for line in lines:
        cave_a, cave_b = line.strip().split("-")
        caves[cave_a].append_connected_caves([cave_b])
        caves[cave_b].append_connected_caves([cave_a])

    return caves


def get_all_possible_paths_to_end(
    start_cave: str, caves: Dict[str, Cave], already_traversed_nodes: Dict[str, int], current_path: List[str]
) -> Set[Tuple[str, ...]]:
    if not caves[start_cave].is_large() and (already_traversed_nodes.get(start_cave, 0) > 0):
        return set()
    already_traversed_nodes[start_cave] = already_traversed_nodes.get(start_cave, 0) + 1
    current_path.append(start_cave)
    if start_cave == "end":
        return set([tuple(current_path)])

    paths = []
    for connected_cave in caves[start_cave].connected_caves:
        paths.append(
            get_all_possible_paths_to_end(connected_cave, caves, already_traversed_nodes.copy(), current_path.copy())
        )
    return set().union(*paths)


def part_a(caves) -> int:
    return len(get_all_possible_paths_to_end("start", caves, {}, []))


def part_b(caves) -> int:
    routes = set()
    for cave_to_dupe in caves:
        if cave_to_dupe.islower() and cave_to_dupe != "start" and cave_to_dupe != "end":
            caves_replica = copy.deepcopy(caves)
            caves_replica[f"{cave_to_dupe}2"] = Cave(f"{cave_to_dupe}2", False)
            caves_replica[f"{cave_to_dupe}2"].connected_caves = caves_replica[cave_to_dupe].connected_caves
            for c in caves:
                if cave_to_dupe in caves[c].connected_caves:
                    caves_replica[c].append_connected_caves([f"{cave_to_dupe}2"])
            routes = routes.union(get_all_possible_paths_to_end("start", caves_replica, {}, []))

    new_routes = set()
    for route in routes:
        new_route = tuple([x if x[-1] != "2" else x[:-1] for x in route])
        new_routes.add(new_route)
    return len(new_routes)


if __name__ == "__main__":
    caves = read_inputs("input.txt")
    print(f"Part A: {part_a(caves)}")
    print(f"Part B: {part_b(caves)}")
