from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle, permutations, product, cycle
from collections import Counter
import numpy as np
from copy import deepcopy


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[List[Union[Tuple[int, ]]]]:
    scanners_data = raw_data.strip().split('\n\n')
    all_coordinates = []
    for scanner_i in scanners_data:
        scanner_coordinates = []
        for line in scanner_i.split('\n'):
            line_coordinates = tuple(map(int, re.findall(r'[-]*\d+', line)))
            if len(line_coordinates) < 2:
                continue
            scanner_coordinates.append(line_coordinates)
        all_coordinates.append(scanner_coordinates)
    return all_coordinates


def change_orientation(coordinates: List[Tuple[int, ]],):
    coordinates = deepcopy(coordinates)
    n_dimensions = len(coordinates[0])
    list(permutations(range(3), 3))

    # x could be either x, y, z and each of those could be positive or negative, which gives 3 * 2 options
    # y could then be one of 2 left-over dimensions and again positive or negative, which gives another 2 * 2 options
    # z is the remaining dimension in positive or negative, which gives 1 * 2 options
    # In total that gives: 3 * 2 * 2 * 2 * 1 * 2 = 48 orientations, which is not 24 as described in problem statement

    pass


def compare_coordinates(coordinates_a: List[Tuple[int, ]], coordinates_b: List[Tuple[int, ]]) -> bool:
    """Coordinates of the beacons are relative to the scanner and one out of 24 random orientations.
    The orientation of the scanner remains the same, so we can apply a change of orientation to all the coordinates.
    We are searching for beacons that the scanners have in common. There should be 12 of them overlapping.
    Instead of using the scanner as reference, we can also use a beacon coordinate as reference. Then we assume it
    matches with one of the coordinates of the other scanner. If in some orientation 12 vectors are overlapping, we have
    found the correct orientation and overlapping beacons."""
    # leave orientation of coordinates of A as is

    # change orientation of the coordinates of B

    # assume both scanners now have the correct orientation

    # assume one of the scanned coordinates of both A and B are the same, and use this as reference point
    # express all coordinates of A and B relative to the reference point
    # A and B should have 11 remaining overlapping vectors, since we already assume the reference point overlaps
    # if less than 11, then the reference point does not overlap, pick another reference point
    # if none of the reference points overlap, then the scanners are not in the same orientation
    # if with none of the orientations we can find a suitable reference point and 11 other overlapping vectors, the
    # scanner scan no overlapping region.

    return True


if __name__ == '__main__':
    # Sample data
    RAW = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8
"""

    RAW = """--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1"""
    data = parse_data(RAW)
    print(data)



    # Assert solution is correct

    # Actual data
    # RAW = load_data('input.txt')
    # data = parse_data(RAW)

    # Part 1

    # Part 2
