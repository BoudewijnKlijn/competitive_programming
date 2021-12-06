from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle
from collections import Counter


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data() -> List[int]:
    return list(map(int, RAW.strip().split(',')))


def solve(days=18) -> int:
    new_dict = Counter()
    old_dict = Counter(data)
    for i in range(days):
        new_dict = Counter()
        for k, v in old_dict.items():
            if k == 0:
                new_dict[8] = v
                new_dict[6] += v
                continue

            new_dict[k-1] += v
        old_dict = new_dict
    print(new_dict)
    print(sum(new_dict.values()))
    return sum(new_dict.values())


if __name__ == '__main__':
    RAW = load_data('input.txt')

    # Sample data
    # RAW = """3,4,3,1,2"""

    # Parse data
    data = parse_data()

    print(data)

    # part 1
    # for days in range(1, 100):
    #     print(days, solve(days))

    # assert solve(18) == 26
    # assert solve(80) == 5934

    print(solve(256))
