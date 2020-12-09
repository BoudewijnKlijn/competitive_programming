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


def part1():
    preamble = 25
    for i, n in enumerate(data):
        # print(i, n)
        if i < preamble:
            continue

        # print(is_in_preamble(preamble, i, goal=n))
        if not is_in_preamble(preamble, i, goal=n):
            print(i)
            exit(n)



def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input9.txt'
    data = load_data()
    print(data)
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
