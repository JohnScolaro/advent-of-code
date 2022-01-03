"""
Problem 18 of the Advent-of-Code 2021
"""
from typing import Any, List, Optional
import itertools


class SnailFishNumber:
    def __init__(self, equation: str, parent: Optional["SnailFishNumber"] = None) -> None:
        self.parent = parent
        equation_without_outer_brackets = equation[1:-1]
        nest_level = 0
        i = 0
        while True:
            if nest_level == 0 and equation_without_outer_brackets[i] == ",":
                break
            char = equation_without_outer_brackets[i]
            if char == "[":
                nest_level += 1
            elif char == "]":
                nest_level -= 1
            i += 1
        left_side = equation_without_outer_brackets[:i]
        right_side = equation_without_outer_brackets[i + 1 :]
        if left_side.isdecimal():
            self.left_number = int(left_side)
        else:
            self.left_number = SnailFishNumber(left_side, self)
        if right_side.isdecimal():
            self.right_number = int(right_side)
        else:
            self.right_number = SnailFishNumber(right_side, self)

    def __repr__(self) -> str:
        return f"[{self.left_number},{self.right_number}]"

    def reduce(self) -> None:
        """
        If self is able to be reduced, continue exploding and splitting until
        self is fully reduced.
        """
        while True:
            if self.can_explode():
                self.explode()
                continue
            if self.can_split():
                self.split()
                continue
            break

    def can_explode(self, current_level: int = 0) -> bool:
        if current_level >= 4:
            return True
        if isinstance(self.left_number, int):
            can_left_explode = False
        else:
            can_left_explode = self.left_number.can_explode(current_level + 1)
        if isinstance(self.right_number, int):
            can_right_explode = False
        else:
            can_right_explode = self.right_number.can_explode(current_level + 1)
        return can_left_explode or can_right_explode

    def can_split(self) -> bool:
        can_left_side_split = False
        if isinstance(self.left_number, int):
            if self.left_number > 9:
                return True
        else:
            can_left_side_split = self.left_number.can_split()

        can_right_side_split = False
        if isinstance(self.right_number, int):
            if self.right_number > 9:
                return True
        else:
            can_right_side_split = self.right_number.can_split()

        return can_left_side_split or can_right_side_split

    def explode(self, nest_level: int = 0) -> bool:
        """
        Explodes self. Returns True if that call to explode actually exploded
        otherwise False.
        """
        if nest_level == 4:
            self.parent.add_to_left_value(self.left_number, self)
            self.parent.add_to_right_value(self.right_number, self)
            return True
        if not isinstance(self.left_number, int):
            if self.left_number.explode(nest_level + 1):
                if nest_level == 3:
                    self.left_number = 0
                return True
        if not isinstance(self.right_number, int):
            if self.right_number.explode(nest_level + 1):
                if nest_level == 3:
                    self.right_number = 0
                return True
        return False

    def add_to_left_value(self, n: int, original_node: "SnailFishNumber") -> None:
        """ Adds n to the next left regular number. """
        if original_node == self.parent:
            if isinstance(self.right_number, int):
                self.right_number += n
            else:
                self.right_number.add_to_left_value(n, self)
        elif original_node == self.left_number:
            if self.parent is not None:
                self.parent.add_to_left_value(n, self)
        elif original_node == self.right_number:
            if isinstance(self.left_number, int):
                self.left_number += n
            else:
                self.left_number.add_to_left_value(n, self)

    def add_to_right_value(self, n: int, original_node: "SnailFishNumber") -> None:
        """ Adds n to the next right regular number. """
        if original_node == self.parent:
            if isinstance(self.left_number, int):
                self.left_number += n
            else:
                self.left_number.add_to_right_value(n, self)
        elif original_node == self.right_number:
            if self.parent is not None:
                self.parent.add_to_right_value(n, self)
        elif original_node == self.left_number:
            if isinstance(self.right_number, int):
                self.right_number += n
            else:
                self.right_number.add_to_right_value(n, self)

    def split(self) -> bool:
        """ Splits self. Returns whether or not a split occurred. """
        if isinstance(self.left_number, int):
            if self.left_number > 9:
                new_left = self.left_number // 2
                new_right = (self.left_number // 2) + (self.left_number % 2)
                self.left_number = SnailFishNumber(f"[{new_left},{new_right}]")
                self.left_number.parent = self
                return True
        else:
            if self.left_number.split():
                return True

        if isinstance(self.right_number, int):
            if self.right_number > 9:
                new_left = self.right_number // 2
                new_right = (self.right_number // 2) + (self.right_number % 2)
                self.right_number = SnailFishNumber(f"[{new_left},{new_right}]")
                self.right_number.parent = self
                return True
        else:
            if self.right_number.split():
                return True

        return False


def read_inputs(filename: str) -> List[Any]:
    equations = []
    with open(filename, "r") as fp:
        for line in fp:
            equations.append(line.strip())
    return equations


def calculate_magnitude(number: SnailFishNumber) -> None:
    """ Calculates the magnitude of a snailfish number. """
    left_magnitude = (
        number.left_number if isinstance(number.left_number, int) else calculate_magnitude(number.left_number)
    )
    right_magnitude = (
        number.right_number if isinstance(number.right_number, int) else calculate_magnitude(number.right_number)
    )
    return 3 * left_magnitude + 2 * right_magnitude


def add_and_reduce(equations: List[str]) -> SnailFishNumber:
    equation = SnailFishNumber(equations[0])
    for i in range(1, len(equations)):
        equation_to_add = SnailFishNumber(equations[i])
        new_snail_fish_number = SnailFishNumber("[0,0]")
        new_snail_fish_number.left_number = equation
        new_snail_fish_number.left_number.parent = new_snail_fish_number
        new_snail_fish_number.right_number = equation_to_add
        new_snail_fish_number.right_number.parent = new_snail_fish_number
        new_snail_fish_number.reduce()
        equation = new_snail_fish_number
    return equation


def part_a(equations):
    final_number = add_and_reduce(equations)
    return calculate_magnitude(final_number)


def part_b(equations):
    return max(calculate_magnitude(add_and_reduce([x, y])) for x, y in itertools.permutations(equations, 2))


def test_explodes() -> None:
    test_explode("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
    test_explode("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
    test_explode("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
    test_explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    test_explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")


def test_explode(equation, expected):
    test_equation = SnailFishNumber(equation)
    test_equation.explode()
    assert test_equation.__repr__() == expected


def test_splits() -> None:
    test_split("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    test_split("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")


def test_split(equation, expected):
    test_equation = SnailFishNumber(equation)
    test_equation.split()
    assert test_equation.__repr__() == expected


def test_add_and_reduces() -> None:
    test_add_and_reduce(["[1,1]", "[2,2]", "[3,3]", "[4,4]"], "[[[[1,1],[2,2]],[3,3]],[4,4]]")
    test_add_and_reduce(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"], "[[[[3,0],[5,3]],[4,4]],[5,5]]")
    test_add_and_reduce(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"], "[[[[5,0],[7,4]],[5,5]],[6,6]]")
    test_add_and_reduce(
        [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
        ],
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    )
    test_add_and_reduce(
        [
            "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
            "[[[5,[2,8]],4],[5,[[9,9],0]]]",
            "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
            "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
            "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
            "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
            "[[[[5,4],[7,7]],8],[[8,3],8]]",
            "[[9,3],[[9,9],[6,[4,9]]]]",
            "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
            "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
        ],
        "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]",
    )


def test_add_and_reduce(equations, expected_answer) -> None:
    assert add_and_reduce(equations).__repr__() == expected_answer


def test_magnitudes() -> None:
    test_magnitude("[[1,2],[[3,4],5]]", 143)
    test_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384)
    test_magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445)
    test_magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791)
    test_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137)
    test_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)


def test_magnitude(equation: str, expected_magnitude: int) -> None:
    test_equation = SnailFishNumber(equation)
    assert calculate_magnitude(test_equation) == expected_magnitude


if __name__ == "__main__":
    equations = read_inputs("input.txt")
    fish_numbers = [SnailFishNumber(equation) for equation in equations]

    # test_explodes()
    # test_splits()
    # test_magnitudes()
    # test_add_and_reduces()

    print(f"Part A: {part_a(equations)}")
    print(f"Part B: {part_b(equations)}")
