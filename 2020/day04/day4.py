"""
Solutions for the Advent of Code - Day 4
"""

def parse_input_to_get_passport_data(input_file: str) -> list:
    d = []

    record = {}    
    with open(input_file, 'r') as fp:
        for line in fp:
            if line.isspace():
                d.append(record)
                record = {}
            else:
                line = line.split(' ')
                for element in line:
                    if element.split(':')[1][-1] == '\n':
                        record[element.split(':')[0]] = element.split(':')[1][0:-1]
                    else:
                        record[element.split(':')[0]] = element.split(':')[1]

    d.append(record)
    return d

def get_valid_passports_part_a(passport_list: list) -> int:
    """
    Returns a list of passports valid according to the rules in part a.
    """
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'] # 'cid' is simply not required.
    valid_passports = []
    for passport in passport_list:
        for required_field in required_fields:
            passport_valid_so_far = True
            if required_field not in list(passport.keys()):
                passport_valid_so_far = False
                break
        if passport_valid_so_far:
            valid_passports.append(passport)
    return valid_passports

def further_validation_part_b(passport_list: list) -> list:
    """
    Returns a list of passports valid according to the list in part b.
    """
    valid_passports = []
    
    for passport in passport_list:
        passport_valid_flag = True

        if int(passport['byr']) < 1920 or int(passport['byr']) > 2002:
            passport_valid_flag = False

        if int(passport['iyr']) < 2010 or int(passport['iyr']) > 2020:
            passport_valid_flag = False

        if int(passport['eyr']) < 2020 or int(passport['eyr']) > 2030:
            passport_valid_flag = False

        height_type = passport['hgt'][-2:]
        if height_type != 'cm':
            if height_type != 'in':
                passport_valid_flag = False

        if height_type == 'cm':
            if int(passport['hgt'][:-2]) < 150 or int(passport['hgt'][:-2]) > 193:
                passport_valid_flag = False
        if height_type == 'in':
            if int(passport['hgt'][:-2]) < 59 or int(passport['hgt'][:-2]) > 76:
                passport_valid_flag = False

        hcl = passport['hcl']
        if hcl[0] != '#' or int(hcl[1:], 16) > int('FFFFFF', 16):
            passport_valid_flag = False

        ecl = passport['ecl']
        if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            passport_valid_flag = False

        pid = passport['pid']
        try:
            int(pid)
        except:
            passport_valid_flag = False
        if len(pid) != 9:
            passport_valid_flag = False

        if passport_valid_flag:
            valid_passports.append(passport)

    return valid_passports


if __name__ == "__main__":
    passport_list = parse_input_to_get_passport_data('input.txt')
    valid_passports = get_valid_passports_part_a(passport_list)
    print(len(valid_passports))
    valid_passports = further_validation_part_b(valid_passports)
    print(len(valid_passports))
