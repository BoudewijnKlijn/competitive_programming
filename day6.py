import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n\n')
    return data


def part1(data):
    a1 = 0
    for group in data:
        yes = set()
        for person in group.split():
            yes.update(person)
        a1 += len(yes)
    return a1


def part2(data):
    a2 = 0
    for group in data:
        yes = None
        for person in group.split():
            if yes is None:
                yes = set(person)
            else:
                yes = yes.intersection(set(person))
        a2 += len(yes)
    return a2


def main():
    a1 = part1(data)
    print(a1)

    a2 = part2(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input6.txt'
    data = load_data()
    main()

    # t = timeit.Timer('part1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
