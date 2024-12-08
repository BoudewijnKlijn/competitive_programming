import re
import time
from collections import Counter, deque
from copy import deepcopy
from itertools import cycle
from math import prod


def parse(contents):
    grid = [[char for char in line] for line in contents.split("\n")]
    R, C = get_grid_dimensions(grid)

    # get obstacles, start position and direction
    obstacle_positions = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "#":
                obstacle_positions.add((r, c))
            if grid[r][c] == "^":
                start = (r, c)

    return grid, R, C, obstacle_positions, start


def get_grid_dimensions(grid):
    return len(grid), len(grid[0])


def moving_direction():
    # start facing up, then right, then down, then left. repeat
    for dr, dc in cycle([(-1, 0), (0, 1), (1, 0), (0, -1)]):
        yield dr, dc


def part1(contents):
    grid, R, C, obstacle_positions, start = parse(contents)

    # create path
    path = set()
    path.add(start)
    direction = moving_direction()
    dr, dc = next(direction)
    r, c = start
    while True:
        while (r + dr, c + dc) in obstacle_positions:
            # make turn
            dr, dc = next(direction)
        r += dr
        c += dc
        if r < 0 or r >= R or c < 0 or c >= C:
            break
        path.add((r, c))

    return len(path)


def draw_grid(grid, path, obstacle_tile):
    R, C = get_grid_dimensions(grid)
    tmp_grid = deepcopy(grid)
    for r, c, *_ in path:
        tmp_grid[r][c] = "X"
    tmp_grid[obstacle_tile[0]][obstacle_tile[1]] = "O"
    for r in range(R):
        for c in range(C):
            print(tmp_grid[r][c], end="")
        print()


def part2(contents):
    """Obstacle has to be on the original path, or we would never encounter it.
    First create original path.
    Then starting from the back, insert an obstacle on the path.
    Let the guard move and check if he encounters a previously visited position with same direction.
    """
    grid, R, C, obstacle_positions, start = parse(contents)

    # create original path
    # same as part 1. additionally store order and direction
    original_path = list()
    direction = moving_direction()
    dr, dc = next(direction)
    original_path.append((*start, dr, dc))
    r, c = start
    while True:
        while (r + dr, c + dc) in obstacle_positions:
            # make turn
            dr, dc = next(direction)
        r += dr
        c += dc
        if r < 0 or r >= R or c < 0 or c >= C:
            break
        original_path.append((r, c, dr, dc))

    # insert obstacle in the path
    # run simulation and see if we encounter a previously encountered position + direction
    reverse_original_path = original_path[::-1]
    ans = 0
    # start at 2nd last position, because we need to insert obstacle at the last position
    for i, (start_tile, obstacle_tile) in enumerate(
        zip(reverse_original_path[1:], reverse_original_path[:-1]),
        start=1,
    ):
        print(i, len(original_path))
        r, c, dr, dc = start_tile
        obstacle_positions_new = obstacle_positions.copy()
        obstacle_positions_new.add(tuple(obstacle_tile[:2]))
        current_path = original_path.copy()[:-i]
        current_path_positions = set(
            current_path
        )  # list grows large. set is faster to check

        # align the direction generator with the direction of the last tile
        while (dr, dc) != next(direction):
            pass

        # take steps on the path and see if we encounter visited tile with same direction
        # or false if we leave the board.
        is_cycle = False
        while True:
            while (r + dr, c + dc) in obstacle_positions_new:
                # make turn
                dr, dc = next(direction)
            r += dr
            c += dc
            if r < 0 or r >= R or c < 0 or c >= C:
                break
            if (r, c, dr, dc) in current_path_positions:
                is_cycle = True
                break
            current_path.append((r, c, dr, dc))
            current_path_positions.add((r, c, dr, dc))

        if is_cycle:
            ans += 1
            print("cycle YES")

            draw_grid(grid, current_path, obstacle_tile)
            print()
    return ans


if __name__ == "__main__":

    sample = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    assert part1(sample) == 41

    with open("2024/day6.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 6

    # ans2 = part2(contents)
    # print(ans2)
