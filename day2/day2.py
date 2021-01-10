'''
Solutions for the Advent of Code - Day 2
'''

def n_valid_policy_1(input_file):
    """Returns the number of passwords that pass password policy 1"""
    num_good_files = 0
    with open('input.txt', 'r') as fp:
        for line in fp:
            # String comprehension to pull out useful parts of the string.
            split_line = line.split(' ')
            bounds = split_line[0].split('-')
            lower_bound = int(bounds[0])
            upper_bound = int(bounds[1])
            required_letter = split_line[1][0]
            password = split_line[2]

            # Logic to determine if the password passes the rules.
            letter_count = password.count(required_letter)
            if letter_count >= lower_bound and letter_count <= upper_bound:
                num_good_files += 1
                
    return num_good_files

def n_valid_policy_2(input_file):
    """Returns the number of passwords that pass password policy 2"""
    num_good_files = 0
    with open('input.txt', 'r') as fp:
        for line in fp:
            # String comprehension to pull out useful parts of the string.
            split_line = line.split(' ')
            bounds = split_line[0].split('-')
            x = int(bounds[0])
            y = int(bounds[1])
            required_letter = split_line[1][0]
            password = split_line[2]

            n = 0
            if (password[x - 1] == required_letter):
                n += 1
            if (password[y - 1] == required_letter):
                n += 1

            if n == 1:
                num_good_files += 1

    return num_good_files

if __name__ == "__main__":
    print(n_valid_policy_1('input.txt'))
    print(n_valid_policy_2('input.txt'))