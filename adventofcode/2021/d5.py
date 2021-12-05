from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data() -> List[Tuple[int, int, int, int]]:
    pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
    matches = re.findall(pattern, RAW)
    matches = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2 in matches]
    return matches


def solve(is_part1=True):
    """Determine which points are covered and how often.
    Maintain dict with point coordinates and number of times they are covered.
    For part 1 only consider vertical and horizontal lines, so x1 = x2 or y1 = y2."""
    covered = defaultdict(int)
    for x1, y1, x2, y2 in data:
        if is_part1 and (x1 != x2) and (y1 != y2):
            # For part 1 only consider vertical and horizontal lines
            continue

        xs = range(x1, x2 + 1, 1) if x2 >= x1 else range(x1, x2 - 1, -1)
        ys = range(y1, y2 + 1, 1) if y2 >= y1 else range(y1, y2 - 1, -1)

        # Use cycle to avoid exhausting the smaller list.
        zip_list = list(zip(cycle(xs), ys) if len(ys) > len(xs) else zip(xs, cycle(ys)))

        for x, y in zip_list:
            covered[(x, y)] += 1
    return len([v for v in covered.values() if v >= 2])


if __name__ == '__main__':
    RAW = load_data('day5.txt')

    # Sample data
#     RAW = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2"""

    # Parse data
    data = parse_data()

    # Part 1
    print(f'Part 1: {solve(is_part1=True)}')

    # Part 2
    print(f'Part 2: {solve(is_part1=False)}')
