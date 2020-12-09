import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split()))
    return data


def parse_data():
    pass


def is_in_preamble(preamble, pos, goal):
    s = set(data[pos-preamble: pos])
    for n1 in s:
        if (n2 := goal - n1) in s and n2 != n1:
            return n1, n2


def contiguous_set(maxi, needle):
    for begin in range(maxi):
        for end in range(begin+3, maxi):
            if (sum_ := sum(data[begin: end])) > needle:
                break

            if needle == sum_:
                return min(data[begin: end]) + max(data[begin: end])


def part1():
    preamble = 25
    for i, n in enumerate(data):
        if i < preamble:
            continue
        if is_in_preamble(preamble, pos=i, goal=n) is None:
            return n, i


def part2(weakness, maxi):
    return contiguous_set(maxi, weakness)


def main():
    a1, i = part1()
    print(f'{a1=}, {i=}')

    a2 = part2(a1, maxi=i)
    print(a2)


if __name__ == '__main__':
    input_file = 'input9.txt'
    data = load_data()
    parsed = parse_data()
    main()

    t = timeit.Timer('part1()', globals=globals())
    n = 10000
    # t = timeit.Timer('part2(weakness=27911108, maxi=509)', globals=globals())
    # n = 100
    print(sum(t.repeat(repeat=n, number=1)) / n)
