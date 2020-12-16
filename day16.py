import timeit
import re
import numpy as np
from functools import reduce
import math


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip()
    return data


def parse_data():
    # print(data)
    data_segments = data.split('\n\n')
    # (data_segments)
    ranges = dict()
    for line in data_segments[0].split('\n'):
        # print(line)
        name = line.split(':')[0]
        ints = re.findall(r'[\d]+', line)
        assert len(ints) == 4
        ints = map(int, ints)
        ranges[name] = set(range(next(ints), next(ints) + 1)).union(set(range(next(ints), next(ints) + 1)))

    # your (my) ticket
    my_ticket = list()
    for i, line in enumerate(data_segments[1].split('\n')):
        if i == 0:
            continue
        my_ticket = list(map(int, line.split(',')))
        # print(my_ticket)

    # nearby tickets
    nearby_tickets = list()
    for i, line in enumerate(data_segments[2].split('\n')):
        if i == 0:
            continue
        nearby_tickets.append(list(map(int, line.split(','))))
        # print(nearby_tickets)

    return ranges, np.array(my_ticket), np.array(nearby_tickets)


def part1():
    ranges, my_ticket, nearby_tickets = parsed
    # ranges_combined = reduce(lambda x, y: x.union(y), (low.union(high) for (low, high) in ranges.values()))
    ranges_combined = reduce(lambda x, y: x.union(y), ranges.values())

    invalid_sum = 0
    delete_rows = set()
    for i, nearby_ticket in enumerate(nearby_tickets.tolist()):
        for value in nearby_ticket:
            if value not in ranges_combined:
                invalid_sum += value
                delete_rows.add(i)

    return invalid_sum, delete_rows


def part2(delete):
    ranges, my_ticket, nearby_tickets = parsed

    # remove invalid tickets
    nearby_tickets = np.array([nearby_ticket for i, nearby_ticket in enumerate(nearby_tickets) if i not in delete])
    nearby_tickets = np.vstack((nearby_tickets, my_ticket))
    # print(nearby_tickets)
    # print(nearby_tickets[:, 0])

    # determine possible names per position
    all_names = set(ranges.keys())
    # print(all_names)
    correct_names = dict()
    while all_names:
        for pos in range(len(nearby_tickets[0])):
            # print(pos)
            valid_names = set()
            for name, range_values in ranges.items():
                if name not in all_names:
                    continue
                # low, high = range_values
                # print(low)
                # print([i in range_values for i in nearby_tickets[:, pos]])
                if all([i in range_values for i in nearby_tickets[:, pos]]):
                    valid_names.add(name)
                    # print(name)

            if len(valid_names) == 1:
                all_names -= valid_names
                correct_names[list(valid_names)[0]] = pos

    return math.prod([int(my_ticket[col]) for name, col in correct_names.items() if 'departure' in name])


def main():
    a1, delete = part1()
    print(a1)

    a2 = part2(delete)
    print(a2)


if __name__ == '__main__':
    input_file = 'input16.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2_faster(n_total=2020)', globals=globals())
    # n = 1000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
