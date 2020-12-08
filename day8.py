import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data():
    parsed = list()
    for line in data:
        operation, argument = line.split()
        parsed.append((operation, int(argument)))
    return parsed


# def rule_set(operation, argument):
#     if operation == 'acc':
#         return 1
#     elif operation == 'jmp':
#         return argument
#     elif operation == 'nop':
#         return 1


def part1():
    accumulator = 0
    position = 0
    been = set()
    while position not in been:
        been.add(position)
        operation, argument = parsed[position]
        if operation == 'acc':
            accumulator += argument
            position += 1
        elif operation == 'jmp':
            position += argument
        elif operation == 'nop':
            position += 1

    return accumulator


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input8.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
