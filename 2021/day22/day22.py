"""
Problem 22 of the Advent-of-Code 2021
"""


from typing import List, Literal, Set, Union
import dataclasses
import more_itertools


@dataclasses.dataclass(frozen=True)
class Prism:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def intersected_by(self, prism: "Prism") -> bool:
        """
        Boolean returned indicated whether or not another prism cuts into us.
        """
        # return (
        #     ((self.x_min <= prism.x_min <= self.x_max) or (self.x_min <= prism.x_max <= self.x_max))
        #     and ((self.y_min <= prism.y_min <= self.y_max) or (self.y_min <= prism.y_max <= self.y_max))
        #     and ((self.z_min <= prism.z_min <= self.z_max) or (self.z_min <= prism.z_max <= self.z_max))
        # )

        x_intersection = (self.x_max >= prism.x_min) and (prism.x_max >= self.x_min)
        y_intersection = (self.y_max >= prism.y_min) and (prism.y_max >= self.y_min)
        z_intersection = (self.z_max >= prism.z_min) and (prism.z_max >= self.z_min)
        return x_intersection and y_intersection and z_intersection

    def sub_prisms(self, prism: "Prism") -> Set["Prism"]:
        """
        Splits the current prism into many sub_prisms based on another prism
        so that the sub-prisms are either fully contained, or not contained at
        all.
        """

        x_splits = []
        y_splits = []
        z_splits = []

        if self.x_min < prism.x_min <= self.x_max:
            x_splits.append(prism.x_min)
        if self.y_min < prism.y_min <= self.y_max:
            y_splits.append(prism.y_min)
        if self.z_min < prism.z_min <= self.z_max:
            z_splits.append(prism.z_min)

        if self.x_min <= prism.x_max < self.x_max:
            x_splits.append(prism.x_max + 1)
        if self.y_min <= prism.y_max < self.y_max:
            y_splits.append(prism.y_max + 1)
        if self.z_min <= prism.z_max < self.z_max:
            z_splits.append(prism.z_max + 1)

        x_splits = [self.x_min] + x_splits + [self.x_max + 1]
        y_splits = [self.y_min] + y_splits + [self.y_max + 1]
        z_splits = [self.z_min] + z_splits + [self.z_max + 1]

        sub_prisms = set()
        for x_min, x_max in more_itertools.windowed(x_splits, 2):
            for y_min, y_max in more_itertools.windowed(y_splits, 2):
                for z_min, z_max in more_itertools.windowed(z_splits, 2):
                    sub_prisms.add(
                        Prism(
                            x_min=x_min,
                            x_max=x_max - 1,
                            y_min=y_min,
                            y_max=y_max - 1,
                            z_min=z_min,
                            z_max=z_max - 1,
                        )
                    )
        return sub_prisms

    def is_wholly_contained_by(self, prism: "Prism") -> bool:
        return (
            (prism.x_min <= self.x_min)
            and (prism.x_max >= self.x_max)
            and (prism.y_min <= self.y_min)
            and (prism.y_max >= self.y_max)
            and (prism.z_min <= self.z_min)
            and (prism.z_max >= self.z_max)
        )


@dataclasses.dataclass
class Instruction:
    operation: Union[Literal["on"], Literal["off"]]
    prism: Prism


def read_inputs(filename: str) -> List[int]:
    instructions = []
    with open(filename, "r") as fp:
        for line in fp:
            line = line.split(" ")
            on_off = line[0]
            coords = line[1]
            x, y, z = coords.split(",")
            x_min, x_max = map(int, x[2:].split(".."))
            y_min, y_max = map(int, y[2:].split(".."))
            z_min, z_max = map(int, z[2:].split(".."))
            instructions.append(
                Instruction(
                    operation=on_off,
                    prism=Prism(
                        x_min=x_min,
                        x_max=x_max,
                        y_min=y_min,
                        y_max=y_max,
                        z_min=z_min,
                        z_max=z_max,
                    ),
                )
            )

    return instructions


def part_a(instructions: List[Instruction]) -> int:
    # Part 1 only process first 20 instructions
    instructions = instructions[:20]

    on_prisms = process_instructions(instructions)
    return sum(map(get_prism_size, on_prisms))


def part_b(instructions: List[Instruction]) -> int:
    on_prisms = process_instructions(instructions)
    return sum(map(get_prism_size, on_prisms))


def process_instructions(instructions: List[Instruction]):
    on_prisms: Set[Prism] = set()

    for instruction in instructions:
        if instruction.operation == "on":
            on_prisms = add_a_prism(on_prisms, instruction.prism)
        if instruction.operation == "off":
            on_prisms = remove_a_prism(on_prisms, instruction.prism)

    return on_prisms


def add_a_prism(on_prisms: Set[Prism], prism_to_add: Prism) -> Set[Prism]:
    fake_prisms = {prism_to_add}

    # Remove all the prisms that are on from the new prism before adding the
    # subprisms created by this process.
    for on_prism in on_prisms:
        fake_prisms = remove_a_prism(fake_prisms, on_prism)

    return on_prisms.union(fake_prisms)


def remove_a_prism(on_prisms: Set[Prism], prism_to_remove: Prism) -> Set[Prism]:
    prisms_to_remove = set()
    prisms_to_add = set()
    for prism in on_prisms:
        if prism.is_wholly_contained_by(prism_to_remove):
            prisms_to_remove.add(prism)
        elif prism.intersected_by(prism_to_remove):
            sub_prisms = prism.sub_prisms(prism_to_remove)
            for sub_prism in sub_prisms:
                if not sub_prism.is_wholly_contained_by(prism_to_remove):
                    prisms_to_add.add(sub_prism)
            prisms_to_remove.add(prism)

    return (on_prisms - prisms_to_remove).union(prisms_to_add)


def get_prism_size(prism: Prism) -> int:
    return (
        (abs(prism.x_max - prism.x_min) + 1)
        * (abs(prism.y_max - prism.y_min) + 1)
        * (abs(prism.z_max - prism.z_min) + 1)
    )


if __name__ == "__main__":
    instructions = read_inputs("input.txt")

    print(f"Part A: {part_a(instructions)}")
    print(f"Part B: {part_b(instructions)}")
