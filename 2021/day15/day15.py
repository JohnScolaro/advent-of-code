"""
Problem 15 of the Advent-of-Code 2021
"""
from typing import Any, List, Tuple
from queue import PriorityQueue


def read_inputs(filename: str) -> List[Any]:
    lines = []
    with open(filename, "r") as fp:
        for line in fp:
            lines.append([int(x) for x in list(line.strip())])

    return lines


def part_a(lines) -> int:
    path = compute_path((0, 0), (99, 99), lines)
    return sum(lines[x][y] for x, y in path[:-1])


def part_b(lines) -> int:
    lines = modify_lines_for_part_b(lines)
    path = compute_path((0, 0), (499, 499), lines)
    return sum(lines[x][y] for x, y in path[:-1])


def compute_path(start, end, lines) -> List[Tuple[int, int]]:
    explored_coords = set()
    came_from = {}
    queue = PriorityQueue()
    cheapest_cost_to = {}
    queue.put((heuristic(start, end, came_from, lines), start))

    while True:
        _, point = queue.get()
        if point == end:
            break
        explored_coords.add(point)
        for x, y in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            new_point = (point[0] + x, point[1] + y)
            if new_point[0] < 0 or new_point[1] < 0 or new_point[0] >= len(lines) or new_point[1] >= len(lines[0]):
                continue
            if new_point in explored_coords:
                continue
            tentative_priority = heuristic(point, end, came_from, lines) + lines[new_point[0]][new_point[1]]
            if x == -1 or y == -1:
                tentative_priority += 1
            if x == 1 or y == 1:
                tentative_priority -= 1
            if tentative_priority < cheapest_cost_to.get(new_point, 10000000):
                cheapest_cost_to[new_point] = tentative_priority
                came_from[new_point] = point
                queue.put((heuristic(new_point, end, came_from, lines), new_point))

    return back_calculate_path(end, came_from, lines)


def back_calculate_path(point, came_from, lines):
    start = (0, 0)
    path = [point]
    if point == start:
        return path
    while True:
        point = came_from[point]
        path.append(point)
        if point == start:
            break
    return path


def heuristic(coords, end_point, came_from, lines) -> int:
    cx, cy = coords
    ex, ey = end_point
    return abs(cx - ex) + abs(cy - ey) + sum(lines[x][y] for x, y in back_calculate_path(coords, came_from, lines)[:-1])


def modify_lines_for_part_b(lines):
    new_lines = [[0 for _ in range(500)] for _ in range(500)]
    for tile_x in range(5):
        for tile_y in range(5):
            for x in range(100):
                for y in range(100):
                    intermediate_tile_value = lines[x][y] + tile_x + tile_y
                    if intermediate_tile_value > 9:
                        intermediate_tile_value -= 9
                    new_lines[(tile_x * 100) + x][(tile_y * 100) + y] = intermediate_tile_value
    return new_lines


if __name__ == "__main__":
    lines = read_inputs("input.txt")
    print(f"Part A: {part_a(lines)}")
    print(f"Part B: {part_b(lines)}")
