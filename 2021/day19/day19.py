"""
Problem 19 of the Advent-of-Code 2021
"""

from typing import Dict, Generator, Iterator, List, Optional, Set, Tuple
from typing_extensions import final
import dataclasses
import itertools


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int


@dataclasses.dataclass
class Scanner:
    scanner_number: int
    beacons: Set[Point]
    absolute_position: Optional[Point] = None


def beacon_rotation_generator(beacon: Point) -> Generator[Point, None, None]:
    """
    Generate all the 24 different valid positions that a beacon could exist in
    given the unspecified orientation of the scanner.
    """
    tmp = Point(beacon.x, beacon.y, beacon.z)
    for _ in range(3):  # Which direction z points in
        for _ in range(2):  # Positive or negative
            yield Point(tmp.x, tmp.y, tmp.z)
            yield Point(-tmp.y, tmp.x, tmp.z)
            yield Point(-tmp.x, -tmp.y, tmp.z)
            yield Point(tmp.y, -tmp.x, tmp.z)
            tmp = Point(x=-tmp.x, y=tmp.y, z=-tmp.z)  # Flip to opposite z direction.
        tmp = Point(x=tmp.y, y=tmp.z, z=tmp.x)  # Point z at a different axis.


def beacon_field_rotation_generator(beacons: Set[Point]) -> Generator[Set[Point], None, None]:
    """
    Generates all the rotated points for a set of beacons.
    """
    generators = [beacon_rotation_generator(beacon) for beacon in beacons]
    for rotated_field in zip(*generators):
        yield set(rotated_field)


def read_inputs(filename: str) -> Dict[int, Scanner]:
    with open(filename, "r") as fp:
        all_text = fp.read()
    scanners = all_text.split("\n\n")

    processed_scanners = {}
    for i, scanner in enumerate(scanners):
        points = []
        for line in scanner.split("\n")[1:]:
            x, y, z = line.split(",")
            points.append(Point(x=int(x), y=int(y), z=int(z)))
        processed_scanners[i] = Scanner(scanner_number=i, beacons=set(points))
    return processed_scanners


def beacon_field_offset_generator(
    locked_beacons: Set[Point], unlocked_beacons: Set[Point]
) -> Generator[Tuple[Point, Set[Point]], None, None]:
    """
    In order to compare each beacon field with one other to see if they align,
    there is no point comparing all of the 1000*1000*1000 locations the beacons
    could be in to see if they align, because that's a large number of checks.
    Instead we only need to check locations where at least one beacon aligns
    already. To do this we generate every possible pair of beacons between two
    clouds and then move the unlocked beacons so that it's selected beacon from
    the pair is aligned with the selected beacon from the locked cloud.

    We yield the offset, and the entire cloud with that offset applied as a
    tuple.
    """
    for locked_beacon, unlocked_beacon in itertools.product(locked_beacons, unlocked_beacons):
        # Locked_beacon = (3, 4, 5)
        # Unlocked_beacon = (-1, -2, -3)

        # if these are the same point, then the offset is (3 - (-1), 4 - (-2), 5 - (-3))
        # = (4, 6, 8)
        offset = Point(
            x=locked_beacon.x - unlocked_beacon.x,
            y=locked_beacon.y - unlocked_beacon.y,
            z=locked_beacon.z - unlocked_beacon.z,
        )
        offset_field = set(
            Point(x=unlocked_beacon.x + offset.x, y=unlocked_beacon.y + offset.y, z=unlocked_beacon.z + offset.z)
            for unlocked_beacon in unlocked_beacons
        )
        yield (offset, offset_field)


def do_fields_overlap(locked_beacons: Set[Point], unlocked_beacons: Set[Point]) -> bool:
    """
    Fields overlap if 12 or more points between them are shared.
    """
    return len(locked_beacons.intersection(unlocked_beacons)) >= 12


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def scanner_offset_calculator(scanners: Dict[int, Scanner]) -> None:
    remaining_scanners = set(scanners.keys())

    # Lock in first scanner
    scanners[0].absolute_position = Point(x=0, y=0, z=0)
    locked_beacons = scanners[0].beacons
    remaining_scanners.remove(0)

    matched = False
    while remaining_scanners:
        for remaining_scanner_number in remaining_scanners.copy():
            scanner = scanners[remaining_scanner_number]
            for rotated_field in beacon_field_rotation_generator(scanner.beacons):
                for offset, offset_field in beacon_field_offset_generator(locked_beacons, rotated_field):
                    if do_fields_overlap(locked_beacons, offset_field):
                        locked_beacons = locked_beacons.union(offset_field)
                        scanner.absolute_position = offset
                        remaining_scanners.remove(scanner.scanner_number)
                        print(f"Matched Scanner: {scanner.scanner_number}")
                        matched = True
                        break
                if matched:
                    matched = False
                    break
        print(f"Remaining Scanners: {remaining_scanners}")

    print(f"Part A: {len(locked_beacons)}")
    print(
        f"Part B: {max(manhattan_distance(a.absolute_position, b.absolute_position) for a, b in itertools.combinations(scanners.values(), 2))}"
    )


if __name__ == "__main__":
    scanners = read_inputs("input.txt")
    scanner_offset_calculator(scanners)
