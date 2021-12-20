from typing import Tuple, Set
from collections import defaultdict
from itertools import product
from typing import Tuple, List


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    enhancement_data, image_data = raw_data.split('\n\n')
    assert len(enhancement_data) == 512
    return enhancement_data, image_data


def get_enhancements(enhancement_data: str) -> Set[int]:
    enhancements = set()
    for i, char in enumerate(enhancement_data.strip()):
        if char == '#':
            enhancements.add(i)
    return enhancements


def make_grid(image_data: str) -> Set[Tuple[int, int]]:
    grid = set()
    for r, line in enumerate(image_data.strip().split('\n')):
        for c, char in enumerate(line):
            if char == '#':
                grid.add((r, c))
    return grid


def get_neighbors(position: Tuple[int, int]) -> List[Tuple[int, int]]:
    r, c = position
    neighbors = list()
    for dr, dc in product([-1, 0, 1], repeat=2):
        neighbors.append((r + dr, c + dc))
    return neighbors


def enhance(grid, enhancements):
    """Any value that has at least one non-zero neighbor can become one."""
    possible_non_zero = set()
    for position in grid:
        possible_non_zero.update(get_neighbors(position))

    new_grid = set()
    for position in possible_non_zero:
        binary_value = ''
        for n in get_neighbors(position):
            if n in grid:
                binary_value += '1'
            else:
                binary_value += '0'

        sum_neighbors = int(binary_value, 2)
        if sum_neighbors in enhancements:
            new_grid.add(position)
    return new_grid


def part1():
    enhancement_data, image_data = parse_data(RAW)
    enhancements = get_enhancements(enhancement_data)
    grid = make_grid(image_data)
    print(len(grid))
    print_grid(grid)
    for _ in range(2):
        grid = enhance(grid, enhancements)
        print(len(grid))
        print_grid(grid)
    return len(grid)


def print_grid(grid: Set[Tuple[int, int]]):
    """Make visual representation of grid."""
    min_r, min_c = map(min, zip(*grid))
    max_r, max_c = map(max, zip(*grid))
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) in grid:
                print('#', end='')
            else:
                print('.', end='')
        print()  # new line


if __name__ == '__main__':
    # Sample data
    RAW = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    # Assert solution is correct
    assert part1() == 35

    # Actual data
    RAW = load_data('input.txt')

    # # Part 1
    print(part1())
