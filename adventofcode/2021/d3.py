import re
from typing import List, Tuple


def load_data(filename) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().strip().split('\n')


if __name__ == '__main__':
    input_file = 'input.txt'
    data = load_data(input_file)

    # Part 1
    verticals = list(map(''.join, (zip(*data))))

    binary = ''
    for col in verticals:
        zero_count = col.count('0')
        one_count = col.count('1')
        if zero_count > one_count:
            binary += '0'
        else:
            binary += '1'

    gamma = int(int(binary, 2))

    binary = ''
    for col in verticals:
        zero_count = col.count('0')
        one_count = col.count('1')
        if zero_count < one_count:
            binary += '0'
        else:
            binary += '1'

    epsilon = int(int(binary, 2))

    print(gamma * epsilon)
