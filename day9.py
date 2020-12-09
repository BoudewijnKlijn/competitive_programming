import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split()))
    return data


def parse_data():
    pass


def is_in_preamble(preamble, pos, goal=2020):
    s = set(data[pos-preamble: pos])
    for n1 in data:
        if (n2 := goal - n1) in s and n2 != n1:
            return n1, n2


def contiguous_set(maxi, needle):
    for begin in range(maxi):
        for end in range(begin+3, maxi):
            if needle == sum(data[begin: end]):
                return min(data[begin: end]) + max(data[begin: end])


def part1():
    preamble = 25
    for i, n in enumerate(data):
        if i < preamble:
            continue

        if not is_in_preamble(preamble, i, goal=n):
            return n, i


def part2(weakness, maxi):
    return contiguous_set(maxi, weakness)


def main():
    a1, i = part1()
    print(a1)
    # a1, i = 127, 16

    a2 = part2(a1, maxi=i)
    print(a2)


if __name__ == '__main__':
    input_file = 'input9.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
