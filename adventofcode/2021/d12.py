from dataclasses import dataclass
import re
from typing import List, Tuple, Union, Dict, Set
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np
from functools import reduce
from queue import Queue


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[Tuple[str, str]]:
    pattern = re.compile(r'(\w+)-(\w+)')
    return re.findall(pattern, raw_data)


def make_grid() -> Dict[str, Set[str]]:
    grid = defaultdict(set)
    for source, destination in data:
        grid[source].add(destination)
        grid[destination].add(source)
    return grid


def make_cave_types(grid: Dict[str, Set[str]]) -> Tuple[Set[str], Set[str], Set[str]]:
    all_grid_values = reduce(set.union, grid.values())
    all_caves = set(grid.keys()).union(all_grid_values)
    small_caves = {c for c in all_caves if c == c.lower()}
    large_caves = all_caves - small_caves
    return all_caves, small_caves, large_caves


START_CAVE = 'start'
END_CAVE = 'end'


def part1():
    """Can only visit small caves at most once. Large caves can be visited multiple time.
    How many distinct paths can we make?
    Iterative function with queue of destinations."""
    paths = paths_from_node_given_visited(node=START_CAVE, visited=set())
    return len(paths)


def paths_from_node_given_visited(node: str, visited: Set[str]) -> List[List[str]]:
    """How can I move further from the current path?
    The last item is the last node visited."""
    visited_copy = visited.copy()
    # print(node, visited)
    if node == END_CAVE:
        # Do not move further
        return [[node]]

    visited_copy.add(node)


    possible_destinations = set()
    for destination in grid[node]:
        if destination in small_caves and destination in visited_copy:
            # Small caves that are already visited are not added to possible destinations.
            continue
        possible_destinations.add(destination)
    # print(possible_destinations)

    all_future_paths = list()
    while possible_destinations:

        # Add destination to current path, and move further from there.
        destination = possible_destinations.pop()
        future_paths_from_node = paths_from_node_given_visited(destination, visited_copy)
        all_future_paths.extend([[node] + path for path in future_paths_from_node])
    return all_future_paths


if __name__ == '__main__':
    # Sample data
    RAW = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    RAW = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

    RAW = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
    data = parse_data(RAW)

    grid = make_grid()
    all_caves, small_caves, large_caves = make_cave_types(grid)

    # Assert solution is correct
    assert part1() == 226

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    grid = make_grid()
    all_caves, small_caves, large_caves = make_cave_types(grid)

    # Part 1
    print(f'Part 1: {part1()}')

    # Part 2
