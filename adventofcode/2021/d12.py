from dataclasses import dataclass
import re
from typing import List, Tuple, Union, Dict, Set
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np
from functools import reduce
from queue import Queue
from copy import deepcopy


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
    """Can only visit small caves at most once. Large caves can be visited multiple times.
    How many distinct paths can we make?"""
    paths = paths_from_node_given_visited(node=START_CAVE, visited=defaultdict(int), is_part1=True)
    return len(paths)


def part2():
    """Can visit small caves at most twice. Large caves can be visited multiple times.
    How many distinct paths can we make?"""
    paths = paths_from_node_given_visited(node=START_CAVE, visited=defaultdict(int), is_part1=False)
    return len(paths)


def paths_from_node_given_visited(node: str, visited: Dict[str, int], is_part1: bool) -> List[List[str]]:
    """How can I move further from the current path?
    The last item is the last node visited."""
    visited_copy = visited.copy()
    if node == END_CAVE:
        # Do not move further
        return [[node]]

    visited_copy[node] += 1

    possible_destinations = set()
    for destination in grid[node]:
        if destination == START_CAVE:
            # Start cave can never be a destination.
            continue
        elif is_part1 is True and destination in small_caves and visited_copy[destination] >= 1:
            # Small caves that are already visited are not added to possible destinations.
            continue
        elif is_part1 is False and destination in small_caves and visited_copy[destination] >= 1 \
                and max([visited_copy[k] for k in small_caves]) == 2:
            # Only one small cave can be visited twice.
            continue
        possible_destinations.add(destination)

    all_future_paths = list()
    while possible_destinations:
        # Add destination to current path, and move further from there.
        destination = possible_destinations.pop()
        future_paths_from_node = paths_from_node_given_visited(destination, visited_copy, is_part1)
        all_future_paths.extend([[node] + path for path in future_paths_from_node])
    return all_future_paths


if __name__ == '__main__':
    # Sample data
    RAW1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    RAW2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

    RAW3 = """fs-end
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

    for raw, ans1, ans2 in zip((RAW1, RAW2, RAW3), (10, 19, 226), (36, 103, 3509)):
        data = parse_data(raw)
        grid = make_grid()
        all_caves, small_caves, large_caves = make_cave_types(grid)

        # Assert solution is correct
        assert part1() == ans1, 'Test 1 fails'
        assert part2() == ans2, 'Test 2 fails'
    print('All tests pass')

    # Actual data
    RAW = load_data('day12.txt')
    data = parse_data(RAW)

    grid = make_grid()
    all_caves, small_caves, large_caves = make_cave_types(grid)

    # Part 1
    print(f'Part 1: {part1()}')

    # Part 2
    print(f'Part 2: {part2()}')
