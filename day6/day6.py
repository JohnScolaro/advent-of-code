'''
Solve for day6's problem of the advent of code.
'''

def get_inputs(input_file: str) -> list:
    list_of_groups = []
    with open('input.txt', 'r') as fp:
        list_of_people = []
        for line in fp:
            if line.isspace():
                list_of_groups.append(list_of_people)
                list_of_people = []
            else:
                list_of_people.append(line[:-1])
        list_of_groups.append(list_of_people)
    return list_of_groups

if __name__ == "__main__":
    groups = get_inputs('input.txt')

    # Part A
    num_yes_in_group = []
    for group in groups:
        questions_answered_yes_to = ''
        for person in group:
            for letter in person:
                if letter not in questions_answered_yes_to:
                    questions_answered_yes_to += letter
        num_yes_in_group.append(len(questions_answered_yes_to))
    print(sum(num_yes_in_group))

    # Part B
    num_yes_in_group = []
    for group in groups:
        group_string = 'abcdefghijklmnopqrstuvwxyz'
        for person in group:
            person_string = ''
            for letter in person:
                if letter in group_string:
                    person_string += letter
            group_string = person_string
        num_yes_in_group.append(len(group_string))
    print(sum(num_yes_in_group))

        
        

