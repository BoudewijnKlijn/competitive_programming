from abc import abstractmethod
from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[int]:
    return list(map(int, raw_data.strip().split(',')))


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


class Transmission:
    def __init__(self, hexadecimal: str):
        self.hexadecimal = hexadecimal
        self.bits = ''.join(HEX_TO_BIN_MAPPING[c] for c in hexadecimal)
        self.pointer = 0
        self.packets = []

    def decode(self):
        Packet(self.bits[self.pointer:]).decode()


    def read_n(self, n: int) -> str:
        out = ''.join(self.bits[self.pointer + 1: self.pointer + n])
        self.pointer += n
        return out


class Packet:
    def __init__(self, bits: str):
        self.bits = bits
        self.version = bin_to_decimal(self.bits[0:3])
        self.type_id = bin_to_decimal(self.bits[3:6])
        self.decoded = False

    @abstractmethod
    def decode(self):
        raise NotImplementedError


class Literal(Packet):
    def __init__(self, hexadecimal: str):
        super().__init__(hexadecimal)
        self.type_name = 'LITERAL'
        self.literal_value = int()

    def decode(self):
        groups = []
        pointer = 6
        while True:
            groups.append(self.bits[pointer:pointer + 5])
            pointer += 5
            if groups[-1][0] == '0':
                break
        binary_representation_groups = ''.join([g[1:] for g in groups])
        self.literal_value = bin_to_decimal(binary_representation_groups)

        self.decoded = True
        return self


class Operator(Packet):
    def __init__(self, hexadecimal: str):
        super().__init__(hexadecimal)
        self.type_name = 'OPERATOR'
        self.sub_packets = list()
        self.length_type_id = self.bits[6]

    def decode(self):

        if self.length_type_id == '0':
            """If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits 
            of the sub-packets contained by this packet."""
            self.sub_packet_length_in_bits = bin_to_decimal(self.bits[7:22])
            self.sub_packets_bits = self.bits[22:22 + self.sub_packet_length_in_bits]
            Packet(bits=self.sub_packets_bits)
        else:
            # read next 11 bits
            self.n_sub_packets = int()

        self.decoded = True
        return self


def bin_to_decimal(bin_str: str) -> int:
    return int(bin_str, 2)


def part1(hexadecimal: str):
    bits = ''.join(HEX_TO_BIN_MAPPING[c] for c in hexadecimal)
    p = Packet(bits)
    try:
        print(p.literal_value)
    except AttributeError:
        pass

    try:
        print(p.sub_packet_length_in_bits)
    except AttributeError:
        pass


def get_literal_value(bits, pointer):
    groups = list()
    # keep adding groups until we reach a group with a 0 in the first position
    while len(groups) == 0 or groups[-1][0] == '1':
        group, pointer = bits[pointer: pointer + 5], pointer + 5
        groups.append(group)

    # ignore the first bit, and use the others to build the binary representation
    binary_representation = ''.join([g[1:] for g in groups])
    literal_value = bin_to_decimal(binary_representation)
    return literal_value, pointer


def decode(pointer: int) -> int:
    """Decodes the bits starting from the pointer."""
    version, pointer = bin_to_decimal(bits[pointer: pointer + 3]), pointer + 3
    version_sum[0] += version
    type_id, pointer = bin_to_decimal(bits[pointer: pointer + 3]), pointer + 3
    print(f'Version: {version}, type_id: {type_id}')
    if type_id == 4:
        """Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number."""
        literal_value, pointer = get_literal_value(bits, pointer)
        print(f'LITERAL: {literal_value}')
    else:
        """Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some 
        calculation on one or more sub-packets contained within."""
        print(f'OPERATOR...')
        length_type_id, pointer = bits[pointer], pointer + 1
        if length_type_id == '0':
            """If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits 
            of the sub-packets contained by this packet."""
            sub_packet_length_in_bits, pointer = bin_to_decimal(bits[pointer: pointer + 15]), pointer + 15
            pointer_goal = pointer + sub_packet_length_in_bits
            while pointer < pointer_goal:
                pointer = decode(pointer)
        else:
            """If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets 
            immediately contained by this packet."""
            n_sub_packets, pointer = bin_to_decimal(bits[pointer: pointer + 11]), pointer + 11
            for _ in range(n_sub_packets):
                pointer = decode(pointer)
    return pointer


if __name__ == '__main__':
    # Sample data
    RAW = "D2FE28"
    RAW = "38006F45291200"
    RAW = "EE00D40C823060"

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
        decode(pointer=0)
        assert version_sum[0] == answer
    print("All tests pass.")

    # Actual data
    hexadecimal_string = load_data('input.txt').strip()
    bits = ''.join(HEX_TO_BIN_MAPPING[c] for c in hexadecimal_string.strip())
    version_sum = [0]  # to make it globally accessible
    decode(0)
    print(version_sum[0])