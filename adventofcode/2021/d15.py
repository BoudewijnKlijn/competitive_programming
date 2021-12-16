from collections import defaultdict
from queue import PriorityQueue
from typing import List, Tuple, Dict, Set
import time


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[str]:
    return raw_data.strip().splitlines()


def get_grid(is_part2: bool) -> Dict[Tuple[int, int], int]:
    """For part 2 the grid is repeated 5x to right and bottom.
    Every time the grid is repeated, risk levels increase with 1.
    Risk level cannot be higher than 9; after 9 it becomes 1."""

    grid = dict()
    for row_i, row in enumerate(data):
        for col_i, col in enumerate(row):
            for char in col:
                grid[(row_i, col_i)] = int(char)

    if not is_part2:
        return grid

    rs, cs = zip(*grid.keys())
    n_rows = max(rs) + 1
    n_cols = max(cs) + 1

    # Multiply grid
    grid2 = dict()
    for mr in range(5):
        for mc in range(5):
            for (r, c), value in grid.items():
                new_value = grid[(r, c)] + mr + mc
                grid2[(mr*n_rows + r, mc*n_cols + c)] = new_value if new_value <= 9 else new_value % 9
    return grid2


def print_grid() -> None:
    # find min and max coordinates
    rs, cs = zip(*grid.keys())
    min_r = min(rs)
    max_r = max(rs)
    min_c = min(cs)
    max_c = max(cs)

    # loop over grid and print
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            print(grid[(r, c)], end='')
        print()  # newline


def get_neighbors() -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
    """Make dict with set of neighbor coordinates."""
    neighbors = defaultdict(set)
    DR = [1, -1, 0, 0]
    DC = [0, 0, 1, -1]
    for r, c in grid.keys():
        for dr, dc in zip(DR, DC):
            if (r + dr, c + dc) in grid.keys():
                neighbors[(r, c)].add((r + dr, c + dc))
    return neighbors


def shortest_path() -> int:
    """Get shortest path from start to end. Return sum of risk levels of path."""
    rs, cs = zip(*grid.keys())
    max_r = max(rs)
    max_c = max(cs)

    start_pos = (0, 0)
    end_pos = (max_r, max_c)

    queue = PriorityQueue()
    queue.put((0, start_pos))  # Risk of starting position is not counted.
    visited = {start_pos}
    while queue:
        risk, pos = queue.get()
        if pos == end_pos:
            return risk

        for neighbor in neighbors[pos]:
            if neighbor not in visited:
                queue.put((risk + grid[neighbor], neighbor))
                visited.add(neighbor)


if __name__ == '__main__':
    # Sample data
    RAW = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    data = parse_data(RAW)

    # Assert solution is correct
    grid = get_grid(is_part2=False)
    neighbors = get_neighbors()
    assert shortest_path() == 40

    grid = get_grid(is_part2=True)
    neighbors = get_neighbors()
    assert shortest_path() == 315

    print('Tests pass.')
    # print_grid()

    # Actual data
    RAW = load_data('day15.txt')
    data = parse_data(RAW)

    # Part 1
    grid = get_grid(is_part2=False)
    neighbors = get_neighbors()
    print('Part 1:', shortest_path())

    # Part 2
    start_time = time.time()
    grid = get_grid(is_part2=True)
    neighbors = get_neighbors()
    print('Part 2:', shortest_path())
    print(time.time() - start_time)
