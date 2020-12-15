import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split(',')))
    return data


def parse_data():
    pass


def part1():
    for i in range(2020 - len(data)):
        spoken = data[-1]
        if spoken not in data[:-1]:
            data.append(0)
        else:
            turns_apart = list(reversed(data[:-1])).index(spoken) + 1
            data.append(turns_apart)
    return data[-1]


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input15.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
