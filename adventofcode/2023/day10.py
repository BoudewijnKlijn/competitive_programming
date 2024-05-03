connections = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "S": [(-1, 0), (1, 0), (0, -1), (0, 1)],
    ".": [],
}


def get_starting_point(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                return r, c


def plot(grid, enclosed):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if (r, c) in enclosed:
                print("I", end="")
            else:
                print(cell, end="")
        print()


def part1(content):
    grid = [[c for c in line] for line in content.split("\n")]
    start = get_starting_point(grid)

    steps_to_start = {start: 0}
    queue = [start]
    while queue:
        r, c = queue.pop(0)
        for dr, dc in connections[grid[r][c]]:
            new_r, new_c = r + dr, c + dc
            reverse_connection = (-dr, -dc)
            if (
                0 <= new_r < len(grid)
                and 0 <= new_c < len(grid[0])
                and (new_r, new_c) not in steps_to_start
                and reverse_connection in connections[grid[new_r][new_c]]
            ):
                steps_to_start[new_r, new_c] = steps_to_start[r, c] + 1
                queue.append((new_r, new_c))

    # solve what S is.
    next_to_start = {k: v for k, v in steps_to_start.items() if v == 1}
    possibilities = "LFJ7-|"
    possible = None
    for possible in possibilities:
        next_to = [(start[0] + dr, start[1] + dc) for dr, dc in connections[possible]]
        if all(k in next_to for k in next_to_start.keys()):
            break

    return max(steps_to_start.values()), steps_to_start.keys(), possible


def part2(content):
    """Move from top to bottom over the grid.
    When we encounter a '-', the tiles below are enclosed.
    When we encounter another '-' the tiles are not enclosed anymore.
    Special care needs to be taken for corners.
    We have to encounter a '7' or 'F' to open a corner.
    Thereafter, depending on whether we go left or right, tiles may or may not be enclosed.
    """
    grid = [[c for c in line] for line in content.split("\n")]
    _, loop_tiles, s_replacement = part1(content)

    nr = len(grid)
    nc = len(grid[0])

    enclosed = set()

    for col in range(nc):
        in_loop = False
        open_corner = None
        for row in range(nr):
            cell = grid[row][col]

            # Replace S with the correct shape.
            if cell == "S":
                cell = s_replacement

            # Loop tiles can never be enclosed.
            if (row, col) in loop_tiles:
                if cell == "-":
                    in_loop = not in_loop

                # Corner can be opened with F or 7, since we start from the top and move down.
                elif cell in "F7":
                    open_corner = cell
                # When L or J is encountered, we can close the corner.
                elif cell == "L":
                    if open_corner == "7":
                        in_loop = not in_loop
                    open_corner = None
                elif cell == "J":
                    if open_corner == "F":
                        in_loop = not in_loop
                    open_corner = None

            elif in_loop:
                enclosed.add((row, col))

    # plot(grid, enclosed)

    return len(enclosed)


if __name__ == "__main__":

    SAMPLE = """.....
.S-7.
.|.|.
.L-J.
....."""

    SAMPLE2 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

    SAMPLE3 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

    SAMPLE4 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

    SAMPLE5 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

    SAMPLE6 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

    assert part1(SAMPLE)[0] == 4

    assert part1(SAMPLE2)[0] == 4

    assert part1(SAMPLE3)[0] == 8

    with open("day10.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT)[0])

    assert part2(SAMPLE4) == 4

    assert part2(SAMPLE5) == 8

    assert part2(SAMPLE6) == 10

    print(part2(CONTENT))
