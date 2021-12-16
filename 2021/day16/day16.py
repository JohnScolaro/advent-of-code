"""
Problem 16 of the Advent-of-Code 2021
"""
from typing import Any, List


def read_inputs(filename: str) -> List[Any]:
    line = []
    with open(filename, "r") as fp:
        for line in fp:
            return line


def convert_hex_string_to_bin_string(line: str) -> str:
    return "".join(map(lambda x: format(int(x, 16), "04b"), (letter for letter in line)))


def parser(line: str) -> List[Any]:
    """
    The parser returns a packet object. If the parser realise there is a sub-
    packet, then it simply calls itself on that packet to get the packet object
    for that data too.
    """
    version = int(line[0:3], 2)
    type = int(line[3:6], 2)

    if type == 4:
        # Literal
        whole_number: str = ""
        i = 0
        while True:
            additional_bits = line[(i * 5) + 6 : (i * 5) + 11]
            whole_number += additional_bits[1:]
            if additional_bits[0] == "0":
                break
            i += 1
        return {
            "version": version,
            "type": type,
            "subpackets": [],
            "literal": int(whole_number, 2),
            "size": (i * 5) + 11,
        }
    else:
        # Operator
        length_type = int(line[6])
        if length_type == 0:
            # Length Type Operator
            total_length_of_subpackets = int(line[7:22], 2)
            subpackets = []
            start_of_data = 22
            while sum(s["size"] for s in subpackets) < total_length_of_subpackets:
                subpackets.append(parser(line[start_of_data:]))
                start_of_data += subpackets[-1]["size"]
        else:
            # Subpacket Count Type Operator
            num_subpackets = int(line[7:18], 2)
            subpackets = []
            start_of_data = 18
            while len(subpackets) < num_subpackets:
                subpackets.append(parser(line[start_of_data:]))
                start_of_data += subpackets[-1]["size"]
        return {"version": version, "type": type, "subpackets": subpackets, "size": start_of_data}


def operate(packet):
    packet_type = packet["type"]
    if packet_type == 0:
        # Sum
        return sum(operate(p) for p in packet["subpackets"])
    elif packet_type == 1:
        # Product
        i = 1
        for p in packet["subpackets"]:
            i *= operate(p)
        return i
    elif packet_type == 2:
        # Minimum
        return min(operate(p) for p in packet["subpackets"])
    elif packet_type == 3:
        # Maximum
        return max(operate(p) for p in packet["subpackets"])
    elif packet_type == 4:
        # Literal
        return packet["literal"]
    elif packet_type == 5:
        # Greater than
        return 1 if operate(packet["subpackets"][0]) > operate(packet["subpackets"][1]) else 0
    elif packet_type == 6:
        # Less than
        return 1 if operate(packet["subpackets"][0]) < operate(packet["subpackets"][1]) else 0
    elif packet_type == 7:
        # Equal to
        return 1 if operate(packet["subpackets"][0]) == operate(packet["subpackets"][1]) else 0


def get_sum_of_versions(packet):
    return sum(get_sum_of_versions(p) for p in packet["subpackets"]) + packet["version"]


if __name__ == "__main__":
    line = read_inputs("input.txt")
    binary_line = convert_hex_string_to_bin_string(line)
    packet = parser(binary_line)

    print(f"Part A: {get_sum_of_versions(packet)}")
    print(f"Part B: {operate(packet)}")
