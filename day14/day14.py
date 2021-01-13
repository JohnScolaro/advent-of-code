'''
Solutions for the Advent of Code - Day 14
'''

class Mask(object):
    """
    I thought that writing the mask as an object might help me for part 2.
    It didn't...
    """
    def __init__(self, mask: str):
        self.mask = mask
        self.or_mask = int(self.mask.replace('X', '0'), 2)
        self.and_mask = int(self.mask.replace('X', '1'), 2)

    def apply_mask(self, input: int) -> int:
        """ Applies the mask to the input and returns the modified number """
        return ((input | self.or_mask) & self.and_mask)

def read_input_file(file_name: str) -> list:
    """ Reads input file and returns it as a list. Removes useless chars. """
    l = []
    with open(file_name, 'r') as fb:
        for line in fb:
            l.append(line[:-1].replace(' ', '').replace('[', '').replace(']', ''))
    return l

def part_a(input_commands: list) -> int:
    """ The main logic for Part A """
    mask = None
    memory = {}
    for command in input_commands:
        if 'mask' in command:
            mask = Mask(command.split('=')[1])
        if 'mem' in command:
            # String parsing
            raw_command = command.replace('[', '').replace(']', '').replace('mem', '')
            address = int(raw_command.split('=')[0])
            value = int(raw_command.split('=')[1])
            # Setting the value
            memory[address] = mask.apply_mask(value)
    return sum(list(memory.values()))

def do_memory_writes(memory: dict, floating_address: str, value: int):
    """
    Given memory (a dict), a floating address (a string with 0's, 1's, and 'X's
    in it), write value to memory for all possible addresses.
    """
    num_xs = floating_address.count('X')
    num_addresses = num_xs**2
    for i in range(num_addresses):
        # Generate the bit's to replace X using variable length string formatting.
        floating_bits = ('{:0' + str(num_xs) + 'b}').format(i)
        # Substitute new bits in for 1's and 0's
        address = floating_address
        for j in range(num_xs):
            address = address.replace('X', floating_bits[j], 1) 
        # Convert address back to an integer
        address = int(address, 2)
        # Write the value to memory
        memory[address] = value

def get_floating_address(command_address: int, mask_str: str):
    """
    Takes a proper address as an integer, and the mask string, and returns a
    'floating address' by applying the mask to it.
    """
    s = ''
    bitwise_command_address = '{:036b}'.format(command_address)
    for i in range(len(bitwise_command_address)):
        bit_to_write = mask_str[i]
        if mask_str[i] == '0':
            bit_to_write = bitwise_command_address[i]
        s += bit_to_write
    return s

def part_b(input_commands: list) -> int:
    """ Implements the logic for Part B """
    memory = {}
    mask = ''
    for command in input_commands:
        if 'mask' in command:
            mask = command.split('=')[1]
        if 'mem' in command:
            raw_command = command.replace('mem', '')
            address = int(raw_command.split('=')[0])
            value = int(raw_command.split('=')[1])
            do_memory_writes(memory, get_floating_address(address, mask), value)
    return sum(list(memory.values()))


if __name__ == "__main__":
    input_commands = read_input_file('input.txt')
    print("Part A: " + str(part_a(input_commands)))
    print("Part B: " + str(part_b(input_commands)))
