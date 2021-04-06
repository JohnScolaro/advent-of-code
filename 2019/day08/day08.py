"""
Problem 8 of the Advent-of-Code 2019
"""


def read_inputs(filename: str) -> str:
    input: str = ''
    with open(filename, 'r') as fp:
        for line in fp:
            input = line
    return input


def part_a(input: str, image_length: int, image_width: int) -> int:
    """ Solves Part A """
    # Get all layers
    image_size = image_length * image_width
    layers = [input[i * image_size:(i * image_size)+image_size] for i in range((len(input) // image_size))]

    # Find number of zeros on each layer.
    num_zeros_on_layer = [layer.count('0') for layer in layers]

    # Get layer with least zeros.
    layer_of_interest = layers[num_zeros_on_layer.index(min(num_zeros_on_layer))]

    return layer_of_interest.count('1') * layer_of_interest.count('2')


def part_b(input: str, image_length: int, image_width: int) -> None:
    """ Solves Part B """
    # Get all layers
    image_size = image_length * image_width
    layers = [input[i * image_size:(i * image_size)+image_size] for i in range((len(input) // image_size))]

    # For each pixel in all layers, create flattened image from top visible pixel.
    flattened_image: str = ''
    for pixel in range(len(layers[0])):
        stack = [layer[pixel] for layer in layers]
        for colour in stack:
            if colour == '0':  # Black
                flattened_image += ' '
                break
            elif colour == '1':  # White
                flattened_image += '#'
                break
            else:
                pass

    # Reshape flattened image into list for printing, and then print.
    reshaped_image = [flattened_image[i * image_length:(i * image_length) + image_length] for i in range(image_width)]
    for row in reshaped_image:
        print(row)


if __name__ == "__main__":
    input = read_inputs('input.txt')
    image_length = 25
    image_width = 6
    print("Part A: {}".format(part_a(input, image_length, image_width)))
    print("Part B:")
    part_b(input, image_length, image_width)
