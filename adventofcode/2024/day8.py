import re
import time
from collections import Counter, deque
from copy import deepcopy
from itertools import combinations, cycle
from math import prod
from operator import add, mul


def parse(contents):
    antennas = dict()
    for r, line in enumerate(contents.split("\n")):
        for c, char in enumerate(line):
            if char == ".":
                continue
            if char not in antennas:
                antennas[char] = set()
            antennas[char].add((r, c))
    R = r + 1
    C = len(line)
    return antennas, R, C


def part1(contents, multipliers=[1, -2]):
    # get antenna types and positions
    antennas, R, C = parse(contents)

    # loop over all pairs of the same antenna type
    antinodes = set()
    for _, antenna_positions in antennas.items():
        for (r1, c1), (r2, c2) in combinations(antenna_positions, 2):
            dr, dc = r1 - r2, c1 - c2
            for multiplier in multipliers:
                new_antinode = rr, cc = (r1 + multiplier * dr, c1 + multiplier * dc)
                if 0 <= rr < R and 0 <= cc < C:
                    antinodes.add(new_antinode)
    return len(antinodes)


def part2(contents):
    return part1(contents, multipliers=range(-50, 50))


if __name__ == "__main__":

    sample = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    assert part1(sample) == 14

    with open("2024/day8.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 34

    ans2 = part2(contents)
    print(ans2)
