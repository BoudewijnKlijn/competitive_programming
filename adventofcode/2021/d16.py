import math
from typing import List, Tuple


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


HEX_TO_BIN_MAPPING = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def bin_to_decimal(bin_str: str) -> int:
    return int(bin_str, 2)


def get_literal_value(pointer):
    groups = list()
    # keep adding groups until we reach a group with a 0 in the first position
    while len(groups) == 0 or groups[-1][0] == '1':
        group, pointer = bits[pointer: pointer + 5], pointer + 5
        groups.append(group)

    # ignore the first bit, and use the others to build the binary representation
    binary_representation = ''.join([g[1:] for g in groups])
    literal_value = bin_to_decimal(binary_representation)
    return literal_value, pointer


def decode(pointer: int) -> Tuple[int, int]:
    """Decodes the bits starting from the pointer."""
    version, pointer = bin_to_decimal(bits[pointer: pointer + 3]), pointer + 3
    version_sum[0] += version
    type_id, pointer = bin_to_decimal(bits[pointer: pointer + 3]), pointer + 3
    if type_id == 4:
        """Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number."""
        literal_value, pointer = get_literal_value(pointer)
    else:
        """Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some 
        calculation on one or more sub-packets contained within."""
        length_type_id, pointer = bits[pointer], pointer + 1
        values = []
        if length_type_id == '0':
            """If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits 
            of the sub-packets contained by this packet."""
            sub_packet_length_in_bits, pointer = bin_to_decimal(bits[pointer: pointer + 15]), pointer + 15
            pointer_goal = pointer + sub_packet_length_in_bits
            while pointer < pointer_goal:
                pointer, new_value = decode(pointer)
                values.append(new_value)
        else:
            """If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets 
            immediately contained by this packet."""
            n_sub_packets, pointer = bin_to_decimal(bits[pointer: pointer + 11]), pointer + 11
            for _ in range(n_sub_packets):
                pointer, new_value = decode(pointer)
                values.append(new_value)
        if type_id == 0:
            """Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If 
            they only have a single sub-packet, their value is the value of the sub-packet."""
            literal_value = sum(values)
        elif type_id == 1:
            """Packets with type ID 1 are product packets - their value is the result of multiplying together the values 
            of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet."""
            literal_value = math.prod(values)
        elif type_id == 2:
            """Packets with type ID 2 are minimum packets - their value is the minimum of the values of their 
            sub-packets."""
            literal_value = min(values)
        elif type_id == 3:
            """Packets with type ID 3 are maximum packets - their value is the maximum of the values of their 
            sub-packets."""
            literal_value = max(values)
        elif type_id == 5:
            """Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet 
            is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have 
            exactly two sub-packets."""
            assert len(values) == 2
            literal_value = 1 if values[0] > values[1] else 0
        elif type_id == 6:
            """Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is 
            less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly
             two sub-packets."""
            assert len(values) == 2
            literal_value = 1 if values[0] < values[1] else 0
        elif type_id == 7:
            """Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is 
            equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly 
            two sub-packets."""
            assert len(values) == 2
            literal_value = 1 if values[0] == values[1] else 0
        else:
            raise ValueError(f'Unknown type ID: {type_id}')
    return pointer, literal_value


if __name__ == '__main__':
    # Sample data
    # RAW = "D2FE28"
    # RAW = "38006F45291200"
    # RAW = "EE00D40C823060"

    # Assert solution is correct for part 1
    SAMPLES = [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ]
    for hexadecimal_string, answer in SAMPLES:
        print(f'{hexadecimal_string} -> {answer}')
        bits = ''.join(HEX_TO_BIN_MAPPING[c] for c in hexadecimal_string.strip())
        version_sum = [0]  # a list to make it globally accessible
        _, _ = decode(pointer=0)
        assert version_sum[0] == answer

    # Assert solution is correct for part 2
    SAMPLES = [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ]
    for hexadecimal_string, expected_answer in SAMPLES:
        print(f'{hexadecimal_string} -> {expected_answer}')
        bits = ''.join(HEX_TO_BIN_MAPPING[c] for c in hexadecimal_string.strip())
        _, ans = decode(pointer=0)
        assert ans == expected_answer
    print("All tests pass.")

    # Actual data
    hexadecimal_string = load_data('day16.txt').strip()
    bits = ''.join(HEX_TO_BIN_MAPPING[c] for c in hexadecimal_string.strip())

    # Part 1
    version_sum = [0]  # a list to make it globally accessible
    _, _ = decode(pointer=0)
    print("Part 1:", version_sum[0])

    # Part 2
    _, ans = decode(pointer=0)
    print("Part 2:", ans)
