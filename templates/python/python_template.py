"""
Problem 1 of the Advent-of-Code 2019
"""

def read_inputs(filename: str):
    l = []
    with open(filename, 'r') as fp:
        for line in fp:
            l.append(int(line.strip()))
    return l

if __name__ == "__main__":
    l = read_inputs('input.txt')
    print(l)
