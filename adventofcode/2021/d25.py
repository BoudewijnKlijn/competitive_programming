import itertools
from typing import Tuple


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    east_facing_cucumbers = set()
    south_facing_cucumbers = set()
    for r, line in enumerate(raw_data.strip().splitlines()):
        for c, char in enumerate(line.strip()):
            if char == '>':
                east_facing_cucumbers.add((r, c))
            elif char == 'v':
                south_facing_cucumbers.add((r, c))
    return east_facing_cucumbers, south_facing_cucumbers


def make_destinations():
    """Cucumbers only move forward and face east or south, so they only move to the right or to the bottom."""
    h_destination = dict()
    v_destination = dict()
    for r in range(ROWS):
        for c in range(COLS):
            h_destination[(r, c)] = (r, (c+1) % COLS)
            v_destination[(r, c)] = ((r + 1) % ROWS, c)
    return h_destination, v_destination


def do_step(east_facing_cucumbers: set, south_facing_cucumbers: set) -> Tuple[set, set]:
    """Cucumbers facing the same direction all move at the same time.
    Cucumber facing east move before the ones facing south."""
    # First the east facing cucumbers move.
    new_east_facing_cucumbers = set()
    for r, c in east_facing_cucumbers:
        destination = h_destination[(r, c)]
        if destination in south_facing_cucumbers or destination in east_facing_cucumbers:
            # The destination is occupied, so the cucumber cannot move and stays at current location.
            new_east_facing_cucumbers.add((r, c))
        else:
            # The spot is empty. The cucumber moves to destination.
            new_east_facing_cucumbers.add(destination)

    # Then the south facing cucumbers move.
    new_south_facing_cucumbers = set()
    for r, c in south_facing_cucumbers:
        destination = v_destination[(r, c)]
        # Use the updated locations of east facing cucumbers to check if the destination is occupied.
        if destination in south_facing_cucumbers or destination in new_east_facing_cucumbers:
            # The destination is occupied, so the cucumber cannot move and stays at current location.
            new_south_facing_cucumbers.add((r, c))
        else:
            # The spot is empty. The cucumber moves to destination.
            new_south_facing_cucumbers.add(destination)

    return new_east_facing_cucumbers, new_south_facing_cucumbers


def part1():
    east_facing_cucumbers, south_facing_cucumbers = parse_data(RAW)
    for step in itertools.count(1):
        new_east_facing_cucumbers, new_south_facing_cucumbers = do_step(east_facing_cucumbers, south_facing_cucumbers)
        if new_east_facing_cucumbers == east_facing_cucumbers and new_south_facing_cucumbers == south_facing_cucumbers:
            break
        east_facing_cucumbers = new_east_facing_cucumbers
        south_facing_cucumbers = new_south_facing_cucumbers
    return step


if __name__ == '__main__':
    # Sample data
    RAW = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
    ROWS = len(RAW.strip().split('\n'))
    COLS = len(RAW.strip().split('\n')[0])
    h_destination, v_destination = make_destinations()

    # Assert solution is correct
    assert part1() == 58

    # Actual data
    RAW = load_data('input.txt')
    ROWS = len(RAW.strip().split('\n'))
    COLS = len(RAW.strip().split('\n')[0])
    h_destination, v_destination = make_destinations()

    # Part 1
    print(f"Part 1: {part1()}")
