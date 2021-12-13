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


def parse_data(raw_data: str) -> Tuple[List[Tuple[int, int]], List[Tuple[str, int]]]:
    # split into map and fold instructions
    map_data, fold_data = raw_data.split('\n\n')
    # split into lines
    # pattern = re.compile(r'\d+')
    coordinates = [tuple(map(int, line.split(','))) for line in map_data.split('\n')]
    pattern = re.compile(r'([yx])=(\d+)')
    fold_instructions = re.findall(pattern, fold_data.strip())
    fold_instructions = [(plane, int(digit)) for plane, digit in fold_instructions]
    return coordinates, fold_instructions


def create_grid():
    grid = defaultdict(int)
    for r, c in coordinates:
        grid[(r, c)] += 1
    return grid


def calc_grid_sum(grid):
    return sum([1 for v in grid.values() if v > 0])


def print_grid():
    # find min and max coordinates
    min_r = None
    max_r = None
    min_c = None
    max_c = None
    for coordinates in grid.keys():
        r, c = coordinates
        if min_r is None or r < min_r:
            min_r = r
        if max_r is None or r > max_r:
            max_r = r
        if min_c is None or c < min_c:
            min_c = c
        if max_c is None or c > max_c:
            max_c = c

    # loop over grid and print
    # for r in range(min_r, max_r + 1):
    for c in range(min_c, max_c + 1):
        for r in range(min_r, max_r + 1):
            if grid[(r, c)] > 0:
                print('#', end='')
            else:
                print('.', end='')
        print()  # newline


def part1():
    # NOTE: I had to switch x and y.
    # use grid and perform the first fold
    for plane, digit in fold_instructions:
        coordinates_to_check = set(grid.keys())
        print(plane, digit)
        if plane == 'x':
            # fold where y == r == digit, so all c remain the same, all r below change
            # perform fold
            # for (r, c), value in grid.items():
            while coordinates_to_check:
                r, c = coordinates_to_check.pop()
                value = grid[(r, c)]
                if r == digit:
                    assert value == 0, "Value on fold should be zero"
                elif r < digit:
                    # nothing changes
                    continue
                elif r > digit:
                    # fold up
                    grid[(2*digit - r, c)] += value
                    del grid[(r, c)]
        elif plane == 'y':
            # fold where x == c == digit, so all r remain the same, all c to right change
            while coordinates_to_check:
                r, c = coordinates_to_check.pop()
                value = grid[(r, c)]
                if c == digit:
                    assert value == 0, "Value on fold should be zero"
                elif c < digit:
                    # nothing changes
                    continue
                elif c > digit:
                    # fold up
                    grid[(r, 2 * digit - c)] += value
                    del grid[(r, c)]

    return calc_grid_sum(grid)


if __name__ == '__main__':
    # Sample data
    RAW = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
    coordinates, fold_instructions = parse_data(RAW)
    print(coordinates, fold_instructions)

    grid = create_grid()
    # print(grid)


    ans = part1()
    print(ans)
    print_grid()

    # Assert solution is correct

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    coordinates, fold_instructions = parse_data(RAW)
    print(coordinates, fold_instructions)

    grid = create_grid()
    print(calc_grid_sum(grid))
    # print(grid)

    ans = part1()
    print(ans)
    print_grid()
    # Part 2

    # ans is AHPRPAUZ
