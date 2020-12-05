import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def part1(data):
    seat_ids = list()

    for seat in data:
        # seat = 'FFFBBBFRRR'
        # find row
        print(seat)
        row_number, col_number = 0, 0
        for i, row_letter in enumerate(seat[:7]):
            print(row_letter)
            if row_letter == 'B':
                row_number += 2 ** (7-i-1)
        print(row_number)

        for i, col_letter in enumerate(seat[7:]):
            print(col_letter)
            if col_letter == 'R':
                col_number += 2 ** (3-i-1)
        print(col_number)

        seat_id = row_number * 8 + col_number
        print(seat_id)
        seat_ids.append(seat_id)
    return max(seat_ids)

def part2(data):
    pass


def main():
    a1 = part1(data)
    print(a1)

    a2 = part2(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input5.txt'
    data = load_data()
    main()

    # t = timeit.Timer('par1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
