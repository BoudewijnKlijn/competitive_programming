import timeit
from itertools import product
from collections import defaultdict


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def parse_data():
    pass


def part1():
    earliest = int(data[0])
    departures = data[1].split(',')
    int_departures = [int(d) for d in departures if d != 'x']
    wait = [a-b for a, b in zip(int_departures, [earliest % d for d in int_departures])]
    index_ = wait.index(min(wait))
    return wait[index_] * int_departures[index_]


def part2():
    departures = [(t, int(d)) for t, d in enumerate(data[1].split(',')) if d != 'x']
    for t in range(2000000):
        if all([(t + t_plus) % bus_id == 0 for t_plus, bus_id in departures]):
            return t


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input13.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
