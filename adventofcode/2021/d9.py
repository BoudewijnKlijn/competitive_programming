from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle, product
from collections import Counter
import numpy as np
import math


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[str]:
    return raw_data.strip().split('\n')


def part1(data: List[str]) -> int:
    values = dict()

    for x, line in enumerate(data):
        for y, digit in enumerate(line):
            values[(x, y)] = int(digit)

    ans = 0
    # Loop over all x, y values
    for (x, y), value in values.items():
        # Get neighboring values
        neighbors = [values.get((x + 1, y), 10), values.get((x - 1, y), 10), values.get((x, y + 1), 10),
                     values.get((x, y - 1), 10)]

        # count how many times values is lower than neighbors
        if all([value < n for n in neighbors]):
            ans += 1 + value

    return ans


def get_basins(data: List[str]) -> List[List[int]]:
    basins = list()
    values = dict()

    n_cols = len(data[0])
    n_rows = len(data)

    for x, line in enumerate(data):
        for y, digit in enumerate(line):
            values[(x, y)] = int(digit)

    neighbor_dict = dict()

    # Loop over all x, y values
    for (x, y), value in values.items():

        # Get neighbors coordinates up , down, left, right
        neighbors = set()
        for dx, dy in product([-1, 0, 1], repeat=2):
            if (dx == 0 and dy == 0 or abs(dx) == 1 and abs(dy) == 1) or values.get((x+dx, y+dy)) is None:
                continue
            neighbors.add((x + dx, y + dy))
        neighbor_dict[(x, y)] = neighbors

    def should_be_in_basin(a, b):
        if values[(a, b)] == 9:
            return False
        else:
            return True

    checked = set()
    # Create new basin. Start with the first value. If not 9 it is part of a basin. If already checked. skip.
    basins = list()
    for (x, y), value in values.items():
        if (x, y) in checked:
            continue

        checked.add((x, y))

        neighbors_to_check = set()
        basin = set()
        if should_be_in_basin(x, y):
            basin.add((x, y))
            neighbors_to_check = neighbors_to_check.union(neighbor_dict[(x, y)]) - checked

        while neighbors_to_check:
            (xn, yn) = neighbors_to_check.pop()
            checked.add((xn, yn))
            if should_be_in_basin(xn, yn):
                basin.add((xn, yn))
                neighbors_to_check = neighbors_to_check.union(neighbor_dict[(xn, yn)]) - checked

        basins.append(basin)

    return basins


if __name__ == '__main__':
    # Sample data
    RAW = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    data = parse_data(RAW)

    # Assert solution is correct
    assert part1(data) == 15

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    print(part1(data))

    basins = get_basins(data)
    basin_lengths = sorted(map(len, basins), reverse=True)
    ans = math.prod(basin_lengths[:3])
    print(ans)


