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


def parse_data(raw_data: str) -> List[int]:
    return list(map(int, raw_data.strip().split(',')))


if __name__ == '__main__':
    # Sample data
    RAW = """16,1,2,0,4,2,7,1,2,14"""
    data = parse_data(RAW)

    # Assert solution is correct

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    def triangle(x):
        return sum(range(0, abs(x)+1))

    best_score = None
    for trial in range(max(data)):
        score = sum(map(lambda x: triangle(x), (np.array(data) - trial * np.ones_like(data))))
        if best_score is None or score < best_score:
            best_score = score
            best_i = trial

    print(best_score)

    # Part 2
