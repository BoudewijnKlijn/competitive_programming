import re
from typing import List, Tuple


def load_data(filename) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().strip().split('\n')


def get_oxygen_row(columns: List[str]) -> int:
    rows_to_check = set(range(len(columns[0])))
    for col in columns:
        col_subset = [char for row_i, char in enumerate(col) if row_i in rows_to_check]
        counts_0, counts_1 = [col_subset.count(s) for s in ['0', '1']]

        # determine starting bit
        if counts_1 >= counts_0:
            starting_bit = '1'
        else:
            starting_bit = '0'
        print(f'{starting_bit=}')

        # keep columns that start with the starting bit
        rows_to_remove = {row_i for row_i, char in enumerate(col) if char != starting_bit}
        rows_to_check -= rows_to_remove

        if len(rows_to_check) == 1:
            for row_i in rows_to_check:
                return row_i


def get_scrubber_rating(columns: List[str]) -> int:
    print(columns)
    rows_to_check = set(range(len(columns[0])))
    print()
    for col in columns:
        print(col)
        col_subset = [char for row_i, char in enumerate(col) if row_i in rows_to_check]
        print(col_subset)
        counts_0, counts_1 = [col_subset.count(s) for s in ['0', '1']]

        print(counts_0, counts_1)

        # determine starting bit
        if counts_0 <= counts_1:
            starting_bit = '0'
        else:
            starting_bit = '1'
        print(f'{starting_bit=}')

        # keep columns that start with the starting bit
        rows_to_remove = {row_i for row_i, char in enumerate(col) if char != starting_bit}
        print(rows_to_remove)
        rows_to_check = rows_to_check - rows_to_remove
        print(rows_to_check)

        if len(rows_to_check) == 1:
            for row_i in rows_to_check:
                return row_i


if __name__ == '__main__':
    input_file = 'input.txt'
    data = load_data(input_file)

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
# 01010""".strip().split('\n')

    print(data)

    # Part 1
    verticals = list(map(''.join, (zip(*data))))
    print(verticals)

    # binary = ''
    # for col in verticals:
    #     zero_count = col.count('0')
    #     one_count = col.count('1')
    #     if zero_count > one_count:
    #         binary += '0'
    #     else:
    #         binary += '1'
    #
    # gamma = int(int(binary, 2))
    #
    # binary = ''
    # for col in verticals:
    #     zero_count = col.count('0')
    #     one_count = col.count('1')
    #     if zero_count < one_count:
    #         binary += '0'
    #     else:
    #         binary += '1'
    #
    # epsilon = int(int(binary, 2))
    #
    # print(gamma * epsilon)


    # Part 2

    oxygen_row = get_oxygen_row(verticals)
    print(oxygen_row)
    oxygen = int(data[oxygen_row], 2)
    print(oxygen)

    print(verticals)

    scrubber_rating_row = get_scrubber_rating(verticals)
    scrubber_rating = int(data[scrubber_rating_row], 2)
    print(scrubber_rating)

    print(oxygen * scrubber_rating)