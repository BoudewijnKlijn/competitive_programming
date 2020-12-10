import timeit
import numpy as np
from collections import Counter


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split()))
    return data


def part1():
    built_in_adapter = max(data) + 3
    sorted_adapters = np.array(sorted(data) + [built_in_adapter])
    difference = sorted_adapters - np.concatenate((np.array([0]), sorted_adapters[:-1]))
    c = Counter(difference)
    return c[1] * c[3]


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input10.txt'
    data = load_data()
    main()

    # t = timeit.Timer('part1()', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
    #
    # t = timeit.Timer('part2(maxi=509, needle=27911108)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
    #
    # t = timeit.Timer('part2_faster(needle=27911108)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
