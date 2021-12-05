from functools import reduce
from typing import List, Union


def load_data(filename) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(content: str) -> List[str]:
    return content.strip().split('\n')


def get_number(name: str) -> int:
    return int(get_binary(name), 2)


def get_binary(name: str) -> str:
    row_ids_to_check = set(range(len(columns[0])))
    binary = ''
    for col in columns:
        if name in ['oxygen', 'scrubber']:
            # Use part of col. Not all rows have to be checked.
            part_of_col = [char for row_id, char in enumerate(col) if row_id in row_ids_to_check]

            # Count the number of zeros and ones.
            zero_count, one_count = get_count(part_of_col)
        else:
            # Count the number of zeros and ones.
            zero_count, one_count = get_count(col)

        # Determine starting bit.
        bit = get_bit(name, zero_count, one_count)
        binary += bit

        if name in ['oxygen', 'scrubber']:
            # Keep columns that start with the starting bit.
            row_ids_to_remove = {row_id for row_id, char in enumerate(col) if char != bit}
            row_ids_to_check -= row_ids_to_remove

            # Stop early if only one row left.
            if len(row_ids_to_check) == 1:
                row_id = reduce(int, row_ids_to_check)
                return data[row_id]
    return binary


def get_bit(name: str, zero_count: int, one_count: int) -> str:
    """Get bit or starting bit."""
    if name in ['gamma', 'oxygen']:
        if zero_count > one_count:
            return '0'
        else:
            return '1'

    elif name in ['epsilon', 'scrubber']:
        if zero_count <= one_count:
            return '0'
        else:
            return '1'

    else:
        raise ValueError(f'Unknown name: {name}')


def get_count(chars: Union[str, List[str]]) -> List[int]:
    """Count the number of zeros and ones in cols."""
    return [chars.count(char) for char in ['0', '1']]


def part1():
    return get_number('gamma') * get_number('epsilon')


def part2():
    return get_number('oxygen') * get_number('scrubber')
    # return get_number('scrubber')


if __name__ == '__main__':
    # Real data
    input_file = 'day3.txt'
    data = load_data(input_file)

#     # Sample data
#     data = """00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010"""

    # Parse input data
    data = parse_data(data)

    # Input data can be seen as rows. Determine columns.
    columns = list(map(''.join, (zip(*data))))

    print("Part 1:", part1())
    print("Part 2:", part2())
