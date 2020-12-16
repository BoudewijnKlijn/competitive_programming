import timeit
import re
import numpy as np
from functools import reduce



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
        ranges[name] = (set(range(next(ints), next(ints) + 1)), set(range(next(ints), next(ints) + 1)))

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

    return ranges, my_ticket, np.array(nearby_tickets)


def part1():
    ranges, my_ticket, nearby_tickets = parsed
    # ranges_combined = set([*map(set.union, (low.union(high) for (low, high) in ranges.values()))])
    ranges_combined = reduce(lambda x, y: x.union(y), (low.union(high) for (low, high) in ranges.values()))
    # print(ranges_combined)

    # print(ranges)
    # print(my_ticket)
    # print(nearby_tickets)

    invalid_sum = 0
    for nearby_ticket in nearby_tickets.tolist():
        for value in nearby_ticket:
            if value not in ranges_combined:
                invalid_sum += value

    return invalid_sum



# valid = False
#     for pos in range(len(nearby_tickets[0])):
#         for name, range_values in ranges.items():
#             low, high = range_values
#             if all((i in low for i in nearby_tickets[:, pos])):
#                 print('valid')
#                 valid = True

def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input16.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2_faster(n_total=2020)', globals=globals())
    # n = 1000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
