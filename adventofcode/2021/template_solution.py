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
    RAW = """3,4,3,1,2"""
    data = parse_data(RAW)

    # Assert solution is correct

    # Actual data
    # RAW = load_data('input.txt')
    # data = parse_data(RAW)

    # Part 1

    # Part 2
