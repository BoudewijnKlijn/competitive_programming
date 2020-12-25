import timeit
from itertools import product
from collections import defaultdict


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data():
    pass


def transform(loop_size, subject_number=7, value=1):
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


def search(init_loop_size=0, init_value=1, keys=None):
    loop_size, value = init_loop_size, init_value
    while value not in keys:
        loop_size += 1
        value *= 7
        value %= 20201227
    return value, loop_size


def part1():
    pub1, pub2 = map(int, data)
    # pub1, pub2 = 5764801, 17807724 # sample

    key_loop_tuples = list()

    value, loop_size = search(keys={pub1, pub2})
    key_loop_tuples.append((value, loop_size))
    assert transform(loop_size=loop_size) == value

    value, loop_size = search(init_loop_size=loop_size, init_value=value, keys={pub1, pub2} - {value})
    key_loop_tuples.append((value, loop_size))

    # mix them up
    return transform(loop_size=key_loop_tuples[1][1], subject_number=key_loop_tuples[0][0])


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input25.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2()', globals=globals())
    # n = 30
    # print(sum(t.repeat(repeat=n, number=1)) / n)
