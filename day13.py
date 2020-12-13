import timeit
from itertools import product
from collections import defaultdict
import math

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
    print(departures)
    for t in range(2000000):
        if all([(t + t_plus) % bus_id == 0 for t_plus, bus_id in departures]):
            return t


def part2_fast():
    """Slightly faster bruteforce, doesnt work"""
    departures = [(t, int(d)) for t, d in enumerate(data[1].split(',')) if d != 'x']

    max_d_t, max_d = sorted(departures, key=lambda x: x[1], reverse=True)[0]

    t = 100000000000000 - max_d_t - max_d
    while True:
        if (t + max_d_t) % max_d == 0:
            break
        t += 1

    while True:
        if all([(t + t_plus) % bus_id == 0 for t_plus, bus_id in departures]):
            return t
        t += max_d


def part2_fast_v2():
    departures = [(t, int(d)) for t, d in enumerate(data[1].split(',')) if d != 'x']
    times, deps = zip(*departures)

    solved = 1
    t = departures[0][0] + departures[0][1]
    increment = math.prod(deps[:solved])
    while True:
        if all([(t + t_plus) % bus_id == 0 for t_plus, bus_id in departures[:solved+1]]):
            solved += 1
            increment = math.prod(deps[:solved])
            if solved == len(deps):
                return t
        t += increment


def main():
    a1 = part1()
    print(a1)

    # a2 = part2()
    # print(a2)

    a2 = part2_fast_v2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input13.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
