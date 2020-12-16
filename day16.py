import timeit
from collections import defaultdict


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split(',')))
    return data


def parse_data():
    pass


def part1():
    pass


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input16.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2_faster(n_total=2020)', globals=globals())
    # n = 1000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
