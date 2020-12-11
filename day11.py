import timeit
from itertools import product


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def part1():
    occupied_seats = set()
    for round in range(1000):  # 1000 is arbitrary. if no answer, increase it
        occupy_next_round = set()
        for seat in seats:
            n_occupied_around = len(adjacent_seats[seat].intersection(occupied_seats))
            if seat not in occupied_seats and n_occupied_around == 0:
                occupy_next_round.add(seat)
            elif seat in occupied_seats and n_occupied_around < 4:
                occupy_next_round.add(seat)

        if occupied_seats == occupy_next_round:
            return len(occupied_seats)

        occupied_seats = occupy_next_round.copy()


def parse_data():
    # spots
    rows, cols = len(data), len(data[0])
    spots = set(product(range(rows), range(cols)))

    # seats
    seats = set()
    for r, line in enumerate(data):
        for c, symbol in enumerate(line):
            if symbol == 'L':
                seats.add((r, c))

    # adjacent seats
    adjacent_seats = dict()
    for seat in seats:
        surrounding_seats = \
            (set(product(range(seat[0]-1, seat[0]+2), range(seat[1]-1, seat[1]+2))) - {seat}).intersection(spots)
        adjacent_seats[seat] = surrounding_seats

    return seats, adjacent_seats


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    # transform input so we can use day 7 solution
    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input11.txt'
    data = load_data()
    seats, adjacent_seats = parse_data()
    main()

    # t = timeit.Timer('part1()', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
