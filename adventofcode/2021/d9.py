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


def get_values():
    """x and y are not the best naming choice. I had better used r and c."""
    values = dict()
    for x, line in enumerate(data):
        for y, digit in enumerate(line):
            values[(x, y)] = int(digit)
    return values


def get_neighbors():
    """Make dict with set of neighbor coordinates."""
    neighbors = defaultdict(set)
    DX = [1, -1, 0, 0]
    DY = [0, 0, 1, -1]
    for x, y in values.keys():
        for dx, dy in zip(DX, DY):
            if (x + dx, y + dy) in values.keys():
                neighbors[(x, y)].add((x + dx, y + dy))
    return neighbors


def part1():
    """Find points that are lower than all their numbers.
    Return the sum of (value + 1)."""
    ans = 0
    for (x, y), value in values.items():
        # check if value of this coordinate is smaller than the value of all neighbors
        if all([value < values.get((xn, yn)) for (xn, yn) in neighbors.get((x, y))]):
            ans += 1 + value
    return ans


def should_be_in_basin(a, b):
    """Only values smaller than 9 should be in a basin."""
    if values[(a, b)] == 9:
        return False
    return True


def get_basins():
    basins = list()
    checked = set()

    # One other loop that loops over all the whole grid. It can skip over all points that are already checked.
    for (x, y), value in values.items():
        if (x, y) in checked:
            continue
        checked.add((x, y))

        neighbors_to_check = set()
        basin = set()
        if should_be_in_basin(x, y):
            basin.add((x, y))
            # Add neighbors to the list of neighbors to check, but remove neighbors that are already checked.
            neighbors_to_check = neighbors_to_check.union(neighbors[(x, y)]) - checked

        # Loop over the direct neighbors of point in outer loop. Remove and check direct neighbors and add indirect
        # neighbors to the set.
        while neighbors_to_check:
            (xn, yn) = neighbors_to_check.pop()
            checked.add((xn, yn))
            if should_be_in_basin(xn, yn):
                basin.add((xn, yn))
                # Add neighbors to the list of neighbors to check, but remove neighbors that are already checked.
                neighbors_to_check = neighbors_to_check.union(neighbors[(xn, yn)]) - checked

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

    # parse the grid. key=coordinate, value=digit
    values = get_values()

    # get coordinates of neighbors of each coordinate
    neighbors = get_neighbors()

    # Assert solution is correct
    assert part1() == 15

    # Actual data
    RAW = load_data('day9.txt')
    data = parse_data(RAW)

    values = get_values()
    neighbors = get_neighbors()

    # Part 1
    print(f"Part 1: {part1()}")

    # Part 2
    basins = get_basins()
    basin_lengths = sorted(map(len, basins), reverse=True)
    p2 = math.prod(basin_lengths[:3])
    print(f"Part 2: {p2}")
