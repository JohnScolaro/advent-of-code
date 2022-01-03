"""
Problem 20 of the Advent-of-Code 2021
"""

from typing import Any, List, Set, Tuple

INPUT_PIXELS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


def read_inputs(filename: str) -> List[Any]:
    with open(filename, "r") as fp:
        text = fp.read().split("\n\n")

    image_enhancement_algorithm = text[0]
    image_list = text[1].strip().split()

    enhancer = set()
    image = set()

    for i, char in enumerate(image_enhancement_algorithm):
        if char == "#":
            enhancer.add(i)

    for r, row in enumerate(image_list):
        for c, char in enumerate(row):
            if char == "#":
                image.add((r, c))

    return (enhancer, image)


def get_pixels_to_test(image: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    pixels_to_test = set()
    for pixel in image:
        for input_pixel in INPUT_PIXELS:
            pixels_to_test.add((pixel[0] + input_pixel[0], pixel[1] + input_pixel[1]))
    return pixels_to_test


def enhanced_pixel_changes_at_location(
    enhancer: Set[int], image: Set[Tuple[int, int]], location: Tuple[int, int], background_value: bool
) -> bool:
    """
    Tells you whether the enhanced image pixel at location (x, y) changes
    compared to the pixel at location (x, y) in the original image.
    """
    original_pixel = not background_value if location in image else background_value

    new_pixel_bin_num = "".join(
        str(int(not background_value))
        if (location[0] + input_pixel[0], location[1] + input_pixel[1]) in image
        else str(int(background_value))
        for input_pixel in INPUT_PIXELS
    )
    dec_num = int(new_pixel_bin_num, 2)
    new_pixel = dec_num in enhancer

    return original_pixel != new_pixel


def enhance(enhancer: Set[int], image: Set[Tuple[int, int]], background_value: bool) -> Set[Tuple[int, int]]:
    pixels_to_test = get_pixels_to_test(image)

    # Get all the pixels that change
    enhanced_changes = set()
    for pixel in pixels_to_test:
        if enhanced_pixel_changes_at_location(enhancer, image, pixel, background_value):
            enhanced_changes.add(pixel)

    # Get all pixels to track in the new image
    pixels_that_become_tracked = enhanced_changes - image
    pixels_that_remain_tracked = image - enhanced_changes
    enhanced_image = pixels_that_become_tracked.union(pixels_that_remain_tracked)

    # Optionally change background value
    background_pixel = (999999, 999999)
    if enhanced_pixel_changes_at_location(enhancer, image, background_pixel, background_value):
        background_value = not background_value
        # If the background value changed we want to track every pixel in pixels_to_test that ISNT in enhanced_image.
        enhanced_image = pixels_to_test - enhanced_image

    return (background_value, enhanced_image)


def part_a(enhancer: Set[int], image: Set[Tuple[int, int]]) -> int:
    background_value = False
    for _ in range(2):
        background_value, image = enhance(enhancer, image, background_value)
    return len(image)


def part_b(enhancer: Set[int], image: Set[Tuple[int, int]]) -> int:
    background_value = False
    for _ in range(50):
        background_value, image = enhance(enhancer, image, background_value)
    return len(image)


if __name__ == "__main__":
    enhancer, image = read_inputs("input.txt")

    print(f"Part A: {part_a(enhancer, image)}")
    print(f"Part B: {part_b(enhancer, image)}")

