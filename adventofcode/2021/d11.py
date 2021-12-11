from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle, product
from collections import Counter
import numpy as np
from queue import PriorityQueue


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[str]:
    return raw_data.strip().splitlines()


def get_grid():
    grid = dict()
    for row_i, row in enumerate(data):
        for col_i, col in enumerate(row):
            for char in col:
                grid[(row_i, col_i)] = int(char)
    return grid


def get_neighbors(grid):
    neighbors = defaultdict(set)
    delta = (-1, 0, 1)
    for (r, c) in grid.keys():
        for dr, dc in product(delta, repeat=2):
            if dr == 0 and dc == 0:
                continue
            if (r + dr, c + dc) in grid.keys():
                neighbors[(r, c)].add((r + dr, c + dc))
    return neighbors


def print_grid(grid):
    sorted_keys = sorted(grid.keys())
    for i, (r, c) in enumerate(sorted_keys):
        if i % 10 == 0:
            print()
        print(grid[(r, c)], end='')


def one_step(grid):
    neighbors = get_neighbors(grid)
    n_flashes = 0

    # increase value with 1
    for pos, value in grid.items():
        grid[pos] = value + 1

    flashed_positions = set()
    while True:
        flashed_anything = False
        for pos, value in grid.items():
            if pos in flashed_positions:
                # don't flash same position twice
                continue
            if value > 9:
                # flash and inrease value of neighbors
                n_flashes += 1
                flashed_anything = True
                flashed_positions.add(pos)
                for neighbor in neighbors[pos]:
                    grid[neighbor] += 1
        if not flashed_anything:
            break

    # reset flashed positions to zero
    for position in flashed_positions:
        grid[position] = 0

    return grid, n_flashes


def part1():
    grid = get_grid()

    n_flashes = 0
    for step in range(100):
        grid, n_flashes_step = one_step(grid)
        n_flashes += n_flashes_step

    return n_flashes


def part2():
    grid = get_grid()
    n_keys = len(grid)

    n_steps = 0
    while True:
        n_steps += 1
        grid, n_flashes_step = one_step(grid)
        if n_flashes_step == n_keys:
            return n_steps


    #     # flash positions if value <= 9. this decreases value of neighbors by 1.
    #     # have to start flashing from the lowest values because this might increase value of neighbors which then
    #     # have to be flashed as well.
    #     q = PriorityQueue()
    #     for position, val in grid.items():
    #         # priority is minus the value, because highest numbers should go first but priority queue is sorts ascending
    #         q.put((val, position))
    #
    #     # flash logic
    #     flashed_positions = set()
    #     while not q.empty():
    #         current_priority, current_position = q.get()
    #         if current_priority <= -9:
    #             # flash if priority is below -9. add it to flashed positions
    #             flashed_positions.add(current_position)
    #
    #             # decrease value of neighbors by 1
    #             current_neighbors = neighbors[current_position]
    #             for neighbor in current_neighbors:
    #                 grid[neighbor] -= 1
    #                 q.put((grid[neighbor], neighbor))
    #
    # # loop through queue
    # # get highest value
    # # get neighbors
    # # if neighbor is not in queue, add it with value of highest value



if __name__ == '__main__':
    # Sample data
    RAW = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    data = parse_data(RAW)

    # Assert solution is correct
    assert part1() == 1656
    assert part2() == 195

    # Actual data
    RAW = load_data('day11.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {part1()}')

    # Part 2
    print(f'Part 2: {part2()}')
