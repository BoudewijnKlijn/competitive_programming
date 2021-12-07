from typing import List

import numpy as np


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[int]:
    return list(map(int, raw_data.strip().split(',')))


def get_score(is_part1: True) -> int:
    """Calculate score. Use different method for part 1 and part 2."""
    def func(x):
        return abs(x)

    if not is_part1:
        def func(x):
            return sum(range(0, abs(x) + 1))

    best_score = None
    for trial in range(max(data)):
        score = sum(map(func, np.array(data) - trial * np.ones_like(data)))
        if best_score is None or score < best_score:
            best_score = score

    return best_score


if __name__ == '__main__':
    # Sample data
    RAW = """16,1,2,0,4,2,7,1,2,14"""
    data = parse_data(RAW)

    # Assert solution is correct
    assert get_score(is_part1=True) == 37
    assert get_score(is_part1=False) == 168

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {get_score(is_part1=True)}')

    # Part 2
    print(f'Part 2: {get_score(is_part1=False)}')
