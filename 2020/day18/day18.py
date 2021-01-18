'''
Solutions for the Advent of Code - Day 18
'''

def read_input(file_name: str):
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            l.append(line.strip())
    return l

if __name__ == "__main__":
    l = read_input('input.txt')
    print(l)