import re
from itertools import product
from typing import List, Tuple, Union


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[List[Union[Tuple[int, int, int]]]]:
    scanners_data = raw_data.strip().split('\n\n')
    all_coordinates = []
    for scanner_i in scanners_data:
        scanner_coordinates = [(int(x), int(y), int(z))
                               for x, y, z in re.findall(r'([\-\d]+),([\-\d]+),([\-\d]+)', scanner_i)]
        all_coordinates.append(scanner_coordinates)
    return all_coordinates


ORIENTATIONS = {
    (1, 2, 3),  # 1 FACING RIGHT (TO X)
    (1, -3, 2),
    (1, -2, -3),
    (1, 3, -2),
    (-3, 2, 1),  # 1 FACING BACK (TO Z)
    (-2, -3, 1),
    (3, -2, 1),
    (2, 3, 1),
    (-1, 2, -3),  # 1 FACING LEFT (TO -X)
    (-1, -3, -2),
    (-1, -2, 3),
    (-1, 3, 2),
    (3, 2, -1),  # 1 FACING FORWARD (TO -Z)
    (2, -3, -1),
    (-3, -2, -1),
    (-2, 3, -1),
    (-2, 1, 3),  # 1 FACING UP (TO Y)
    (-3, 1, -2),
    (2, 1, -3),
    (3, 1, 2),
    (2, -1, 3),  # 1 FACING DOWN (TO -Y)
    (3, -1, -2),
    (-2, -1, -3),
    (-3, -1, 2),
}


def change_orientation(coordinate: Tuple[int, int, int], orientation: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Change orientation of one coordinate.
    Orientation consists of the dimension and its sign."""
    dimensions = tuple(map(lambda o: abs(o) - 1, orientation))
    signs = tuple(map(lambda x: 1 if x > 0 else -1, orientation))
    new_coordinate = signs[0] * coordinate[dimensions[0]], signs[1] * coordinate[dimensions[1]], signs[2] * \
                     coordinate[dimensions[2]]
    return new_coordinate


def change_orientations(coordinates: List[Tuple[int, int, int]], orientation: Tuple[int, int, int]) -> \
        List[Tuple[int, int, int]]:
    """Change orientation of many coordinates.
    Orientation consists of the dimension and its sign."""
    new_coordinates = []
    for coordinate in coordinates:
        new_coordinate = change_orientation(coordinate, orientation)
        new_coordinates.append(new_coordinate)
    return new_coordinates


def get_location_and_orientation(scanner_a: int, scanner_b: int, scanner_location_and_orientation: dict):
    """Coordinates of the beacons are relative to the scanner and one out of 24 random orientations.
    The orientation of the scanner remains the same, so we can apply a change of orientation to all the coordinates.
    We are searching for beacons that the scanners have in common. There should be 12 of them overlapping.
    Instead of using the scanner as reference, we can also use a beacon coordinate as reference. Then we assume it
    matches with one of the coordinates of the other scanner. If in some orientation 12 vectors are overlapping, we have
    found the correct orientation and overlapping beacons.

    # assume one of the scanned coordinates of both A and B are the same, and use this as reference point
    # express all coordinates of A and B relative to the reference point
    # A and B should have 11 remaining overlapping vectors, since we already assume the reference point overlaps
    # if less than 11, then the reference point does not overlap, pick another reference point
    # if none of the reference points overlap, then the scanners are not in the same orientation
    # if with none of the orientations we can find a suitable reference point and 11 other overlapping vectors, the
    # scanner scan no overlapping region."""
    scanner_a_location, scanner_a_orientation = scanner_location_and_orientation[scanner_a]
    coordinates_a = change_orientations(data[scanner_a], scanner_a_orientation)

    for orientation in ORIENTATIONS:
        # Leave orientation of coordinates of A as is and change orientation of the coordinates of B. Assume both
        # scanners now have the same orientation.
        coordinates_b = change_orientations(data[scanner_b], orientation)

        for reference_coordinate_a, reference_coordinate_b in product(coordinates_a, coordinates_b):
            # Assume that the reference point is the same for both scanners.
            # Express all coordinates of A and B relative to the reference point.
            coordinates_a_adjusted = {tuple(map(lambda pos, ref: pos - ref, coordinates, reference_coordinate_a))
                                      for coordinates in coordinates_a if coordinates != reference_coordinate_a}
            coordinates_b_adjusted = {tuple(map(lambda pos, ref: pos - ref, coordinates, reference_coordinate_b))
                                      for coordinates in coordinates_b if coordinates != reference_coordinate_b}
            # A and B should have 11 remaining overlapping vectors, since we already assume the reference point overlaps
            # if less than 11, then the reference point does not overlap, pick another reference point
            if len(coordinates_a_adjusted.intersection(coordinates_b_adjusted)) >= 11:
                # based on the scanner location of a and the reference points we can calculate the new location of b
                location_b = tuple([a + b - c
                                    for a, b, c in
                                    zip(scanner_a_location, reference_coordinate_a, reference_coordinate_b)])
                location_and_orientation = (location_b, orientation)
                return True, location_and_orientation
    return False, None


def get_scanner_location_and_orientation():
    scanner_location_and_orientation = dict()
    unresolved_scanners = set(range(len(data)))
    found_scanners = {(0, ((0, 0, 0), (1, 2, 3)))}
    while True:
        resolved_scanner = found_scanners.pop()
        scanner_i, location_and_orientation = resolved_scanner
        scanner_location_and_orientation[scanner_i] = location_and_orientation
        unresolved_scanners.remove(scanner_i)
        if not unresolved_scanners:
            break

        print(len(unresolved_scanners))
        for scanner_j in unresolved_scanners:
            found_one, found_location_and_orientation = get_location_and_orientation(
                scanner_i, scanner_j, scanner_location_and_orientation
            )
            if found_one:
                found_scanners.add((scanner_j, found_location_and_orientation))

    return scanner_location_and_orientation


def part1(scanner_location_and_orientation):
    beacons = set()
    for scanner_i, location_and_orientation in scanner_location_and_orientation.items():
        scanner_location, scanner_orientation = location_and_orientation
        beacon_coordinates_relative_to_scanner_location = change_orientations(data[scanner_i], scanner_orientation)
        for c in beacon_coordinates_relative_to_scanner_location:
            beacon_coordinates = tuple([a + b for a, b in zip(scanner_location, c)])
            beacons.add(beacon_coordinates)
    return len(beacons)


def part2(scanner_location_and_orientation):
    largest_distance = 0
    for scanner_location_a, _ in scanner_location_and_orientation.values():
        for scanner_location_b, _ in scanner_location_and_orientation.values():
            distance = sum(abs(a - b) for a, b in zip(scanner_location_a, scanner_location_b))
            if distance > largest_distance:
                largest_distance = distance
    return largest_distance


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
    data = parse_data(RAW)
    all_possible_coordinates = list()
    for i, orientation in enumerate(ORIENTATIONS):
        possible = change_orientations(data[0], orientation)
        all_possible_coordinates.append(possible)
    for i in range(len(data)):
        assert data[i] in all_possible_coordinates
    print('Change orientation tests pass.')

    # Assert solution is correct
    RAW = load_data('day19_sample.txt')
    data = parse_data(RAW)
    scanner_location_and_orientation = get_scanner_location_and_orientation()
    assert part1(scanner_location_and_orientation) == 79  # part 1
    assert part2(scanner_location_and_orientation) == 3621  # part 2
    print('Answers for sample are correct.')

    # Actual data
    RAW = load_data('day19.txt')
    data = parse_data(RAW)
    scanner_location_and_orientation = get_scanner_location_and_orientation()

    # Part 1
    print(f'Part 1: {part1(scanner_location_and_orientation)}')

    # Part 2
    print(f'Part 2: {part2(scanner_location_and_orientation)}')
