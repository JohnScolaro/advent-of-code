"""
Problem 17 of the Advent-of-Code 2021
"""
from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    line = []
    with open(filename, "r") as fp:
        for line in fp:
            line = line.strip().split(" ", 2)[-1]
            x = line.split(", ")[0].split("..")
            y = line.split(", ")[1].split("..")
            return ((int(x[0][2:]), int(x[1])), (int(y[0][2:]), int(y[1])))


def get_target_area_coords(x_coords, y_coords):
    return set((i, j) for i in range(x_coords[0], x_coords[1] + 1) for j in range(y_coords[0], y_coords[1] + 1))


def step(coords, velocities):
    new_coords = (coords[0] + velocities[0], coords[1] + velocities[1])
    x_vel = velocities[0]
    y_vel = velocities[1]
    if x_vel < 0:
        x_vel += 1
    elif x_vel > 0:
        x_vel -= 1
    y_vel -= 1

    return (new_coords, (x_vel, y_vel))


def get_steps(initial_velocity, max_x, min_y):
    coords = (0, 0)
    velocity = initial_velocity
    all_coords = set()
    while True:
        coords, velocity = step(coords, velocity)
        if coords[0] > max_x or coords[1] < min_y:
            break
        all_coords.add(coords)
    return all_coords


def part_a(min_y, max_y):
    """
    If we shoot something up with a velocity of 3, then it's y coords go:
        timestep 0: position: 0 velocity: 3
        timestep 1: position: 3 velocity: 2
        timestep 2: position: 5 velocity: 1
        timestep 3: position: 6 velocity: 0
        timestep 4: position: 5 velocity: -1
        timestep 5: position: 3 velocity: -2
        timestep 6: position: 0 velocity: -3
    And you can see that it ends back at the exact start position with a
    velocity that is negative of the shot.

    So the highest shot that hit the target has the largest negative y velocity
    at the start point and hits it. If our target areas y coords are -10 to
    -15, then the fastest we can shoot it down from the starting point is with
    a velocity of -15, and we would just need to back calculate the height of
    a shot with 14 velocity because then the last step will will be at velocity
    -15. We can just use for formula for the sum of consecutive numbers to do
    that.
    """
    n = abs(min_y) - 1
    max_height = (n / 2) * (1 + n)
    return int(max_height)


def part_b(x_coords, y_coords):
    target_area_coords = get_target_area_coords(x_coords, y_coords)
    successful_initial_velocities = set()
    for vx in range(17, x_coords[1] + 1):
        for vy in range(y_coords[0], abs(y_coords[0]) + 1):
            set_of_locations = get_steps((vx, vy), x_coords[1], y_coords[0])
            if set_of_locations.intersection(target_area_coords):
                successful_initial_velocities.add((vx, vy))

    return len(successful_initial_velocities)


if __name__ == "__main__":
    x_coords, y_coords = read_inputs("input.txt")

    print(f"Part A: {part_a(y_coords[0], y_coords[1])}")
    print(f"Part B: {part_b(x_coords, y_coords)}")
