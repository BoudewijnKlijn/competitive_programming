from itertools import product
from typing import Set
from typing import Tuple, List, Dict


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


def make_grid(image_data: str) -> Dict[Tuple[int, int], int]:
    grid = dict()
    for r, line in enumerate(image_data.strip().split('\n')):
        for c, char in enumerate(line):
            if char == '#':
                grid[(r, c)] = 1
            else:
                grid[(r, c)] = 0

    # add border of zeros
    grid = add_border_grid(grid, fill_value=0)
    return grid


def get_neighbors(position: Tuple[int, int]) -> List[Tuple[int, int]]:
    r, c = position
    neighbors = list()
    for dr, dc in product([-1, 0, 1], repeat=2):
        neighbors.append((r + dr, c + dc))
    return neighbors


def enhance(grid: Dict[Tuple[int, int], int], enhancements: Set[int], fill_value: int) -> dict:
    new_grid = dict()
    for position in grid:
        binary_value = ''
        for n in get_neighbors(position):
            if FILLER == 1:
                binary_value += str(grid.get(n, 1 - fill_value))
            else:
                binary_value += str(grid.get(n, 0))

        sum_neighbors = int(binary_value, 2)
        new_grid[position] = 1 if sum_neighbors in enhancements else 0

    # add border
    new_grid = add_border_grid(new_grid, fill_value)
    return new_grid


def add_border_grid(grid, fill_value):
    min_r, min_c = map(min, zip(*grid))
    max_r, max_c = map(max, zip(*grid))

    for c in range(min_c - 1, max_c + 2):
        # top and bottom border
        grid[(min_r - 1, c)] = fill_value
        grid[(max_r + 1, c)] = fill_value
    for r in range(min_r - 1, max_r + 2):
        # left and right border
        grid[(r, min_c - 1)] = fill_value
        grid[(r, max_c + 1)] = fill_value
    return grid


def part1(steps: int) -> int:
    enhancement_data, image_data = parse_data(RAW)
    enhancements = get_enhancements(enhancement_data)
    grid = make_grid(image_data)
    for s in range(steps):
        print(s)
        fill_value = 0
        if FILLER == 1 and (s % 2) == 0:
            fill_value = 1
        grid = enhance(grid, enhancements, fill_value)
    return sum(grid.values())


def print_grid(grid: Dict[Tuple[int, int], int]):
    """Make visual representation of grid."""
    min_r, min_c = map(min, zip(*grid))
    max_r, max_c = map(max, zip(*grid))
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[(r, c)] == 1:
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
    FILLER = 0 if RAW[0] == '.' else 1

    # Assert solution is correct
    assert part1(steps=2) == 35

    # Actual data
    RAW = load_data('day20.txt')
    FILLER = 0 if RAW[0] == '.' else 1

    # Part 1
    print(part1(steps=50))
