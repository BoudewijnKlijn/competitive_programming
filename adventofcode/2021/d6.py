from typing import List
from collections import Counter


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[int]:
    return list(map(int, raw_data.strip().split(',')))


def evolve_one_day(old_dict):
    new_dict = Counter()
    for k, v in old_dict.items():
        if k == 0:
            new_dict[8] = v
            new_dict[6] += v
            continue

        new_dict[k - 1] += v
    return new_dict


def evolve_multiple_days(days) -> int:
    """Evolve for a number of days."""
    old_dict = Counter(data)  # initial state
    for _ in range(days):
        old_dict = evolve_one_day(old_dict)
    return sum(old_dict.values())


if __name__ == '__main__':
    # Sample data
    RAW = """3,4,3,1,2"""
    data = parse_data(RAW)
    assert evolve_multiple_days(18) == 26
    assert evolve_multiple_days(80) == 5934

    # Actual data
    RAW = load_data('day6.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {evolve_multiple_days(80)}')

    # Part 2
    print(f'Part 2: {evolve_multiple_days(256)}')
