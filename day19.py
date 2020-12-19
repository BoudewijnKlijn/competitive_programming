import timeit
import re
from itertools import product
from collections import defaultdict


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n\n')
    return data


def parse_data():
    rules, messages = data

    rules = rules.split('\n')
    parsed_rules = defaultdict(set)

    unsolved_rules = list()
    for rule in rules:
        m = re.match(r'([\d]+): "(.)"', rule)
        if m is not None:
            parsed_rules[m.group(1)].add(m.group(2))
        else:
            unsolved_rules.append(rule)

    pattern = re.compile(r'([\d]+): ([\d]+).?([\d]+)?.?\|?.?([\d]+)?.?([\d]+)?')
    rules = unsolved_rules
    while rules:
        unsolved_rules = list()
        for rule in rules:
            m = pattern.search(rule)
            if all([m.group(g) is None or m.group(g) in parsed_rules for g in range(2, 6)]):
                if m.group(3) is not None:
                    parsed_rules[m.group(1)].update([x + y for x, y in
                                                     product(parsed_rules[m.group(2)], parsed_rules[m.group(3)])])
                else:
                    parsed_rules[m.group(1)].update(parsed_rules[m.group(2)])

                if m.group(4) is not None and m.group(5) is not None:
                    parsed_rules[m.group(1)].update([x + y for x, y in
                                                    product(parsed_rules[m.group(4)], parsed_rules[m.group(5)])])
                elif m.group(4) is not None:
                    parsed_rules[m.group(1)].update(parsed_rules[m.group(4)])

            else:
                unsolved_rules.append(rule)

        rules = unsolved_rules
    return parsed_rules, messages


def part1():
    parsed_rules, messages = parsed
    valid = 0
    for message in messages.split('\n'):
        if message in parsed_rules['0']:
            valid += 1
    return valid


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input19.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
