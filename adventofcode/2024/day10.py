from collections import deque


def parse(contents):
    grid = [[char for char in line] for line in contents.split("\n")]
    return grid


def get_tiles(grid):
    tiles = {i: set() for i in range(10)}
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == ".":
                continue
            tiles[int(char)].add((r, c))
    return tiles


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def part1(contents, distinct_trails=False):
    grid = parse(contents)
    tiles = get_tiles(grid)
    trailheads = tiles[0]

    # paths must go up with just 1 step, and be up, right, down, left. not diagonal
    ans = 0
    for r, c in trailheads:
        summits_reached = list()
        queue = deque([(0, (r, c))])
        while queue:
            value, (r, c) = queue.pop()
            for dr, dc in DIRECTIONS:
                neighbor = (r + dr, c + dc)
                if neighbor in tiles[value + 1]:
                    if value + 1 == 9:
                        summits_reached.append(neighbor)
                    else:
                        queue.append((value + 1, neighbor))

        if not distinct_trails:
            summits_reached = set(summits_reached)
        ans += len(summits_reached)
    return ans


def part2(contents):
    return part1(contents, distinct_trails=True)


if __name__ == "__main__":

    sample = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    assert part1(sample) == 36

    with open("2024/day10.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 81

    ans2 = part2(contents)
    print(ans2)
