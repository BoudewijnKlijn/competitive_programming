import numpy as np
from collections import Counter
from functools import lru_cache


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split()))
    return data


def part1():
    built_in_adapter = max(data) + 3
    sorted_adapters = np.array([0] + sorted(data) + [built_in_adapter])
    difference = sorted_adapters[1:] - sorted_adapters[:-1]
    c = Counter(difference)
    return c[1] * c[3]


def parse_data(data):
    built_in_adapter = max(data) + 3
    sorted_adapters = np.array([0] + sorted(data) + [built_in_adapter])
    d = dict()
    for adapter in sorted_adapters:
        possible = [content for content in range(adapter + 1, adapter + 3 + 1) if content in sorted_adapters]
        counts = [1] * 3  # zip wil remove the excessive ones
        d.update({adapter: dict(zip(possible, counts))})
    return d


# cache = dict()
@lru_cache
def get_number_of_bags(needle):
    # if needle in cache:
    #     return cache[needle]
    if needle == max(parsed.keys()):
        # cache[needle] = 1
        return 1

    contents = parsed.get(needle)
    total = 0
    for needle2, count in contents.items():
        total += count * get_number_of_bags(needle2)

    # cache[needle] = total
    return total


def part2():
    return 1 * get_number_of_bags(0)


def main():
    a1 = part1()
    print(a1)

    # transform input so we can use day 7 solution
    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input10.txt'
    data = load_data()
    parsed = parse_data(data)
    main()

    # t = timeit.Timer('part1()', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
    #
    # t = timeit.Timer('part2()', globals=globals())
    # n = 100000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
    #
    # t = timeit.Timer('part2_faster(needle=27911108)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
