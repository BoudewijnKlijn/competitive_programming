import timeit


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def part1(data):
    seat_ids = list()
    for seat in data:
        row_number, col_number = 0, 0
        for i, row_letter in enumerate(seat[:7]):
            if row_letter == 'B':
                row_number += 2 ** (7-i-1)

        for i, col_letter in enumerate(seat[7:]):
            if col_letter == 'R':
                col_number += 2 ** (3-i-1)

        seat_id = row_number * 8 + col_number
        seat_ids.append(seat_id)
    return seat_ids


def part1_v2(data):
    seat_ids = list()
    for seat in data:
        seat = seat.translate(str.maketrans('FBLR', '0101'))
        row = int(seat[:7], 2)
        col = int(seat[7:], 2)
        seat_id = row * 8 + col
        seat_ids.append(seat_id)
    return seat_ids


def part2(seat_ids):
    min_seat, max_seat = min(seat_ids), max(seat_ids)
    alt = range(min_seat, max_seat+1)
    missing = set(alt) - set(seat_ids)
    return missing


def main():
    seat_ids = part1(data)
    a1 = max(seat_ids)
    print(a1)

    seat_ids = part1_v2(data)
    a1 = max(seat_ids)
    print(a1)

    a2 = part2(seat_ids)
    print(a2)


if __name__ == '__main__':
    input_file = 'input5.txt'
    data = load_data()
    main()

    t = timeit.Timer('part1_v2(data)', globals=globals())
    n = 10000
    print(sum(t.repeat(repeat=n, number=1)) / n)
