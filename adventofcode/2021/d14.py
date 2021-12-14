from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    start, insertion_rules = raw_data.strip().split('\n\n')

    pattern = re.compile(r'([A-Z]+) -> ([A-Z]+)')
    pairs = re.findall(pattern, insertion_rules.strip())

    return start, dict(pairs)


if __name__ == '__main__':
    # Sample data
    RAW = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
    # Actual data
    RAW = load_data('input.txt')
    # data = parse_data(RAW)

    start, pairs = parse_data(RAW)
    print(start, pairs)

    # # part 1
    # def next_step1(start):
    #     new = ''
    #     for x, y in zip(start[:-1], start[1:]):
    #         # print(x, y)
    #         insertion = pairs.get(x+y, '')
    #         new += x + insertion
    #     return new + start[-1]
    #
    # for step in range(10):
    #     start = next_step1(start)
    #
    # c = Counter(start)
    # print(c)
    #
    # a = c.most_common()[0][1]
    # b = c.most_common()[-1][1]
    #
    # # answer part 1
    # print(a - b)

    # part 2
    #
    def next_step(counter_xy):
        new = defaultdict(int)
        for k, v in counter_xy.items():
            insertion = pairs.get(k)
            if insertion is None:
                new[k] += v
            else:
                new[k[0]+insertion] += v
                new[insertion+k[1]] += v
        return new

    xy = list()
    for x, y in zip(start[:-1], start[1:]):
        xy.append(x + y)
    pair_counts = Counter(xy)
    print(pair_counts)

    for step in range(40):
        pair_counts = next_step(pair_counts)

    print(pair_counts)

    final_dict = defaultdict(int)
    final_dict[start[0]] -= 1
    final_dict[start[-1]] = 1
    for k, v in pair_counts.items():
        final_dict[k[0]] += v
        # final_dict[k[1]] += v
    print(final_dict)

    c = Counter(final_dict)
    print(c)

    a = c.most_common()[0][1]
    b = c.most_common()[-1][1]

    # answer part 1
    print(a - b)
