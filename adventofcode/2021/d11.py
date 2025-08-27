from typing import List, Tuple, Dict, Set
from collections import defaultdict
from itertools import product
import time


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[str]:
    return raw_data.strip().splitlines()


def get_grid() -> Dict[Tuple[int, int], int]:
    grid = dict()
    for row_i, row in enumerate(data):
        for col_i, col in enumerate(row):
            for char in col:
                grid[(row_i, col_i)] = int(char)
    return grid


def get_neighbors(grid: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
    neighbors = defaultdict(set)
    delta = (-1, 0, 1)
    for (r, c) in grid.keys():
        for dr, dc in product(delta, repeat=2):
            # Position itself is not a neighbor.
            if dr == 0 and dc == 0:
                continue
            # Neighbor has to be on the grid.
            if (r + dr, c + dc) in grid.keys():
                neighbors[(r, c)].add((r + dr, c + dc))
    return neighbors


def print_grid(grid: Dict[Tuple[int, int], int]) -> None:
    """Print visual representation of the grid."""
    sorted_keys = sorted(grid.keys())
    for i, (r, c) in enumerate(sorted_keys):
        if i % 10 == 0:
            print()
        print(grid[(r, c)], end='')


def one_step(grid: Dict[Tuple[int, int], int]) -> Tuple[Dict[Tuple[int, int], int], int]:
    """Perform one step:
    - First, the energy level of each octopus increases by 1.
    - Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent
    octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level
    greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level
    increased beyond 9. (An octopus can only flash at most once per step.)
    - Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to
    flash."""
    neighbors = get_neighbors(grid)
    n_flashes = 0

    # Increase value with 1
    for pos, value in grid.items():
        grid[pos] = value + 1

    # Flash until no more flashes.
    flashed_positions = set()
    while True:
        flashed_anything = False
        for pos, value in grid.items():

            # Don't flash same position twice.
            if pos in flashed_positions:
                continue

            if value > 9:
                # Flash and increase value of neighbors.
                n_flashes += 1
                flashed_anything = True
                flashed_positions.add(pos)
                for neighbor in neighbors[pos]:
                    grid[neighbor] += 1

        if not flashed_anything:
            break

    # Reset flashed positions to zero.
    for position in flashed_positions:
        grid[position] = 0

    return grid, n_flashes


def one_step_v2(grid: Dict[Tuple[int, int], int]) -> Tuple[Dict[Tuple[int, int], int], int]:
    """This implementation should loop over fewer positions, hence be a bit faster.

    Perform one step:
    - First, the energy level of each octopus increases by 1.
    - Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent
    octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level
    greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level
    increased beyond 9. (An octopus can only flash at most once per step.)
    - Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to
    flash."""
    neighbors = get_neighbors(grid)
    n_flashes = 0
    to_be_flashed_positions_queue = set()
    flashed_positions = set()

    # Increase value with 1
    for pos, value in grid.items():
        grid[pos] = value + 1
        if value == 9:
            to_be_flashed_positions_queue.add(pos)

    # Flash until no more positions to flash.
    while to_be_flashed_positions_queue:
        pos = to_be_flashed_positions_queue.pop()
        if pos in flashed_positions:
            # Don't flash same position twice.
            continue

        # Flash and increase value of neighbors.
        n_flashes += 1
        flashed_positions.add(pos)
        for neighbor in neighbors[pos]:
            grid[neighbor] += 1
            if grid[neighbor] > 9 and neighbor not in flashed_positions:
                to_be_flashed_positions_queue.add(neighbor)

    # Reset flashed positions to zero.
    for position in flashed_positions:
        grid[position] = 0

    return grid, n_flashes


def part1(v2=False):
    """Perform 100 steps and count total flashes in all steps."""
    grid = get_grid()

    n_flashes = 0
    for _ in range(100):
        if not v2:
            grid, n_flashes_step = one_step(grid)
        else:
            grid, n_flashes_step = one_step_v2(grid)
        n_flashes += n_flashes_step

    return n_flashes


def part2(v2=False):
    """Perform steps until all positions flash in the same step.
    Return that step number."""
    grid = get_grid()
    n_keys = len(grid)

    n_steps = 0
    while True:
        n_steps += 1
        if not v2:
            grid, n_flashes_step = one_step(grid)
        else:
            grid, n_flashes_step = one_step_v2(grid)
        if n_flashes_step == n_keys:
            return n_steps


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

    for do_v2 in [False, True]:
        start_time = time.time()
        # Part 1
        print(f'Part 1: {part1(do_v2)}')

        # Part 2
        print(f'Part 2: {part2(do_v2)}')

        print(f'Part 1 & 2: {time.time() - start_time} seconds')
