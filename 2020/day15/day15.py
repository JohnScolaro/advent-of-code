"""
Solutions for the Advent of Code - Day 15
"""

def elf_game(starting_numbers: list, n: int) -> int:
    """
    Returns the n'th number in the sequence.
    Only 'trick' I found was to store times last said in a dictionary?
    Not sure if there was supposed to be a more efficient method of
    calculating the answer, but I just brute forced the 30,000,000th number
    and it took less than 10 seconds?
    """
    # Initialise algorithm
    turn_count = 1
    hist = {}
    for j in starting_numbers[:-1]:
        hist[j] = turn_count
        turn_count += 1
    last_number = starting_numbers[-1]

    # Count through the turns
    while turn_count != n:
        if last_number not in hist:
            this_number = 0
        else:
            this_number = turn_count - hist[last_number]

        hist[last_number] = turn_count
        last_number = this_number
        turn_count += 1

    return this_number

if __name__ == "__main__":
    starting_numbers = [7, 14, 0, 17, 11, 1, 2]
    print("Part A: " + str(elf_game(starting_numbers, 2020)))
    print("Part B: " + str(elf_game(starting_numbers, 30000000)))