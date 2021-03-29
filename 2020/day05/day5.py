"""
Solutions for the Advent of Code - Day 5
"""

if __name__ == "__main__":
    boarding_ids = []
    with open('input.txt', 'r') as fp:
        for line in fp:
            boarding_ids.append(int(line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2))

    # Part A
    print(max(boarding_ids))

    # Part B
    boarding_ids.sort()
    for i in range(len(boarding_ids)):
        if boarding_ids[i + 1] - boarding_ids[i] == 2:
            print(boarding_ids[i] + 1)
            exit(0)
