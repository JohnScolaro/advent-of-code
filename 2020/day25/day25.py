"""
Solutions for the Advent of Code - Day 25
"""

def read_input(file_name: str):
    """ Gets the two public keys from the input file """
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            l.append(line.strip())
    return (int(l[0]), int(l[1]))

def transform_number(subject_number: int, loop_size: int):
    """ Run the subject number through 'loop_size' loops. """
    x = 1
    for _ in range(loop_size):
        x *= subject_number
        x %= 20201227
    return x

def find_loop_size(subject_number: int, public_key: int):
    """
    Run the transform until the pulic key is found, and return the loop size.
    """
    x = 1
    loops = 0
    while x != public_key:
        loops += 1
        x *= subject_number
        x %= 20201227
    return loops

def part_a(key_1: int, key_2: int):
    # Get encryption key
    loop_size = find_loop_size(7, key_1)
    encryption_key = transform_number(key_2, loop_size)

    # Verify encryption key
    loop_size = find_loop_size(7, key_2)
    verify_encryption_key = transform_number(key_1, loop_size)

    # Return encryption key
    if encryption_key != verify_encryption_key:
        print("Encryption keys do not match.")
        return -1
    else:
        return encryption_key

if __name__ == "__main__":
    key_1, key_2 = read_input('input.txt')
    print("Part A: " + str(part_a(key_1, key_2)))