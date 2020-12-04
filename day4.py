import timeit


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def part1(data):
    pass


def part2(data):
    pass


def main():
    a1 = part1(data)
    print(a1)

    a2 = part2(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input4.txt'
    data = load_data()
    main()

    # t = timeit.Timer('par1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
